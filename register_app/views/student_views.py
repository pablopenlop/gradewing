from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Prefetch

from register_app.forms import StudentForm, EnrollmentForm
from register_app.forms import StudentProgrammeForm
from register_app.forms import StudentQualificationForm
from register_app.models import Student, Enrollment 
from register_app.models import StudentProgramme, StudentQualification
from subject_app.models import Qualification
from itertools import chain
from choices import QF
from shared.delete import DeleteForm
import time
from django.db import connection


@login_required
def students(request):
    context = {'url_headerbar': reverse('students-headerbar')}
    return render(request, 'register_app/students/students.html', context)




@login_required
def students_json(request):
    start_time = time.time()

    # Prefetch all necessary related objects
    students = request.user.userprofile.school.students.prefetch_related(
        'tags',
        'enrollments__tags',
        'enrollments__student_qualifications__qualification',
        'enrollments__period',
        'enrollments__yeargroup__school',
        'enrollments__student__programmes',
        'enrollments__student__programmes__qualifications__enrollments',  
    )

    
    students_data = []
    
    for student in students:
        # Cache the reverse URL and student tags
        hx_get_url = reverse('student-infocard', args=[student.id])
        student_tags = [str(tag) for tag in student.tags.all()]
        
        # Evaluate enrollments once to avoid extra queries
        enrollments = list(student.enrollments.all())

        if enrollments:
            for enrollment in enrollments:
                enrollment_tags = [tag.name for tag in enrollment.tags.all()]
                students_data.append({
                    'id': f"{student.id}-{enrollment.id}",
                    'name': enrollment.student.catalog_name,
                    'tags': student_tags + enrollment_tags,
                    'period': str(enrollment.period),
                    'yeargroup': str(enrollment.yeargroup),
                    'programme': ", ".join(enrollment.programmes_with_count()),
                    'qualifications':  [str(qualification) for qualification in enrollment.student_qualifications.all()],
                    'hx_get': hx_get_url,
                    'hx_target': '#student-infocard-container',
                    'hx_swap': 'innerHTML',
                })
               
              
        else:
            students_data.append({
                'id': f"{student.id}-0",
                'name': student.catalog_name,
                'tags': student_tags,
                'period': "Unenrolled",
                'yeargroup': "n/a",
                'programme': [],
                'qualifications': [],
                'hx_get': hx_get_url,
                'hx_target': '#student-infocard-container',
                'hx_swap': 'innerHTML',
            })
    print("Queries:", len(connection.queries))
    print(f"Elapsed time: {time.time() - start_time:.6f} seconds")
    return JsonResponse({'data': students_data})


@login_required
def students_headerbar(request):
    school = request.user.userprofile.school
    populated_periods = (list(
        school.periods
        .filter(enrollments__isnull=False)
        .distinct().values_list('name', flat=True)
    ))
    if school.students.filter(enrollments__isnull=True).exists():
        populated_periods.append("Unenrolled")

    context = {
        'periods': populated_periods,
        'url_general_form': reverse('student-general-form', kwargs={'student_id': 0}),
        'url_table': reverse('students-table')
        }
    return render(request, 'register_app/students/partials/students_headerbar.html', context)

@login_required
def students_table_old(request):
    school = request.user.userprofile.school
    students = school.students.all()    
    students = list(chain(*[students for _ in range(10)]))
    context = {'students': students}
    return render(request, 'register_app/students/partials/students_table.html', context)

@login_required
def students_table(request):
    return render(request, 'register_app/students/partials/students_table_json.html', {})

@login_required
def student_general_form(request, student_id):
    school = request.user.userprofile.school
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        form = StudentForm(initial={'school': school}, school=school)
    else:
        form = StudentForm(instance=student, school=school)
    form.action = reverse('student-general-save')
    form.form_id= "student-general-form"
    return render(
        request, 
        'register_app/students/partials/student_general_form.html', 
        {'form': form}
    )
    

@require_POST
@login_required
def save_student_general(request):
    student_id = request.POST.get('id')
    student = Student.objects.get(id=student_id) if student_id else None
    form = StudentForm(request.POST, instance=student)
    if form.is_valid():
        student=form.save(commit=True)
        student.update_enrollment_tags()
        return JsonResponse({
            'success': True, 
             'redirect_url': reverse('student-editor', kwargs={'student_id': student.id})
            })
    else:
        errors = {field: error[0] for field, error in form.errors.items()}
        error_message = next(iter(errors.values()))
        return JsonResponse({"success": False, "error_message": error_message})
    
    
@login_required
def get_student_infocard(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.url_editor = reverse('student-editor', kwargs={'student_id': student.id})
    student.url_delete_form = reverse('student-delete-form', kwargs={'student_id': student.id})
    return render(
        request, 
        'register_app/students/partials/student_infocard.html', 
        {'student': student}
    )


@login_required
def student_delete_form(request, student_id):
    context = {'form': DeleteForm(model=Student, delete_id=student_id)}
    return render(request, 'partials/delete_form.html', context)

@require_POST    
@login_required
def delete_student(request):
    delete_id = request.POST.get('delete_id')
    try:
        Student.objects.get(id=delete_id).delete()
    except Student.DoesNotExist:
        return JsonResponse(data={}, status=404)
    else:
        return JsonResponse({'success': True})


@login_required
def student_editor(request, student_id):
    context = {'student_id': Student.objects.get(id=student_id).id}
    return render(request, 'register_app/students/student_editor.html', context)

@login_required
def student_general_card(request, student_id):
    student= Student.objects.get(id=student_id)
    student.url_general_form = reverse('student-general-form', kwargs={'student_id': student.id})
    context = {'student': student}
    return render(request, 'register_app/students/partials/student_general_card.html', context)


@login_required
def student_enrollments_card(request, student_id):
    student = (
        Student.objects
        .prefetch_related(Prefetch('enrollments', queryset=Enrollment.objects.only('id'),))
        .get(id=student_id)
    )

    # Add URLs to each enrollment
    for enrollment in student.enrollments.all():
        enrollment.url_form = reverse(
            'student-enrollment-form',
            kwargs={'student_id': student.id, 'enrollment_id': enrollment.id}
        )
        enrollment.url_deleteform = reverse(
            'student-enrollment-delete-form',
            kwargs={'enrollment_id': enrollment.id}
        )
    
    # Generate the URL for creating a new enrollment
    student.url_enrollment_form = reverse(
        'student-enrollment-form',
        kwargs={'student_id': student.id, 'enrollment_id': 0}
    )
    
    context = {'student': student}
    return render(request, 'register_app/students/partials/student_enrollments_card.html', context)


@login_required
def student_enrollment_form(request, student_id, enrollment_id):
    student = Student.objects.get(id=student_id)
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
    except Enrollment.DoesNotExist:
        form = EnrollmentForm(
        student=student, 
        initial={'student': student}
        )
        period_name = None
    else:
        form = EnrollmentForm(
            instance=enrollment, 
            student=student, 
        )
        period_name = enrollment.period.__str__()
    form.action = reverse('student-enrollment-save')
    form.form_id= "student-enrollment-form"

    return render(
        request, 
        'register_app/students/partials/student_enrollment_form.html',
        {'form': form, 'period_name': period_name}
    )

@require_POST
@login_required
def save_student_enrollment(request):
    enrollment_id = request.POST.get('id')
    enrollment = Enrollment.objects.get(id=enrollment_id) if enrollment_id else None
    form = EnrollmentForm(request.POST, instance=enrollment)
    
    if form.is_valid():
        form.save(commit=True)
        return JsonResponse({'success': True})

@login_required
def student_enrollment_delete_form(request, enrollment_id):
    context = {'form': DeleteForm(model=Enrollment, delete_id=enrollment_id)}
    return render(request, 'partials/delete_form.html', context)

@require_POST    
@login_required
def delete_student_enrollment(request):
    delete_id = request.POST.get('delete_id')
    try:
        Enrollment.objects.get(id=delete_id).delete()
    except Enrollment.DoesNotExist:
        return JsonResponse(data={}, status=404)
    else:
        return JsonResponse({'success': True})


@login_required
def student_qualifications_card(request, student_id):
    qualification_queryset = StudentQualification.objects.only('id') 
    programme_queryset = StudentProgramme.objects.prefetch_related(
        Prefetch('qualifications', queryset=qualification_queryset)
    ).only('id') 
    student = (
        Student.objects
        .prefetch_related(Prefetch('programmes', queryset=programme_queryset))
        .only('id')  
        .get(id=student_id)
    )

    for programme in student.programmes.all():
        for sq in programme.qualifications.all():
            sq.url_form = reverse(
                'student-qualification-form',
                kwargs={'programme_id': programme.id, 'sq_id': sq.id}
            )
            sq.url_deleteform = reverse(
                'student-qualification-delete-form',
                kwargs={'sq_id': sq.id}
            )

        programme.url_qualification_form = reverse(
            'student-qualification-form',
            kwargs={'programme_id': programme.id, 'sq_id': 0}
        )

        programme.url_deleteform = reverse(
            'student-programme-delete-form',
            kwargs={'programme_id': programme.id}
        )

    student.url_programme_form = reverse(
        'student-programme-form',
        kwargs={'student_id': student.id}
    )
    context = {'student': student}
    return render(request, 'register_app/students/partials/student_qualifications_card.html', context)


@login_required
def student_programme_form(request, student_id):
    student = Student.objects.get(id=student_id)
    form = StudentProgrammeForm(student=student, initial={'student': student})
    form.action = reverse('student-programme-save')
    form.form_id= "student-programme-form"
    return render(
        request, 
        'register_app/students/partials/student_programme_form.html',
        {'form': form}
    )

@login_required
def save_student_programme(request):
    form = StudentProgrammeForm(request.POST)
    if form.is_valid():
        programme = form.save(commit=True)
        qf= QF.choices_from_values(programme.name)[0]
        qnames = QF.get_core_qualification_names(qf)
        #quals = Qualification.objects.filter(name__in=qnames, core=True)
        quals = Qualification.objects.filter(name__in=qnames)
        for qual in quals:
            StudentQualification.objects.create(programme=programme, qualification=qual)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def student_programme_delete_form(request, programme_id):
    context = {'form': DeleteForm(model=StudentProgramme, delete_id=programme_id)}
    return render(request, 'partials/delete_form.html', context)


@require_POST    
@login_required
def delete_student_programme(request):
    delete_id = request.POST.get('delete_id')
    try:
        StudentProgramme.objects.get(id=delete_id).delete()
    except StudentProgramme.DoesNotExist:
        return JsonResponse(data={}, status=404)
    else:
        return JsonResponse({'success': True})
    
    
@login_required
def student_qualification_form(request, programme_id, sq_id):

    programme = StudentProgramme.objects.get(id=programme_id)
    try:
        sq = StudentQualification.objects.get(id=sq_id)
    except StudentQualification.DoesNotExist:
        form = StudentQualificationForm(
        programme=programme, 
        initial={'programme': programme}
        )
        is_external = False
    else:
        form = StudentQualificationForm(
            instance=sq, 
            programme=programme, 
        )
        is_external = sq.is_external()
    form.action = reverse('student-qualification-save')
    form.form_id= "student-qualification-form"

    return render(
        request, 
        'register_app/students/partials/student_qualification_form.html',
        {'form': form, 'is_external': is_external}
    )

    
    
@login_required
def student_qualification_delete_form(request, sq_id):
    context = {'form': DeleteForm(model=StudentQualification, delete_id=sq_id)}
    return render(request, 'partials/delete_form.html', context)

@require_POST
@login_required
def save_student_qualification(request):
    sq_id = request.POST.get('id')
    sq = StudentQualification.objects.get(id=sq_id) if sq_id else None
    form = StudentQualificationForm(request.POST, instance=sq)
    confirmation = int(request.POST.get('confirmation'))
    
    if form.is_valid():
        if sq and not confirmation:
            current_enrollments = set(form.cleaned_data.get('enrollments'))
            old_enrollments = set(sq.enrollments.all())
            deleted_enrollments = old_enrollments - current_enrollments  
            if deleted_enrollments:
                return JsonResponse({
                    'requires_confirmation': True, 
                    'message': '''
                    One or more enrollment periods have been removed.
                    This will unassign the student from any related checkpoints and classes. 
                    '''
                    })
            
        current_sq = form.save(commit=True)
        if not sq and current_sq.qualification.sub_qualification:
            sub_qualification = current_sq.qualification.sub_qualification
            sq_sub, created = StudentQualification.objects.update_or_create(
                programme = current_sq.programme,
                qualification = sub_qualification,
                    defaults={}
            )
            current_sq.sub_qualification = sq_sub
            current_sq.save() 
        
        return JsonResponse({'success': True})

@require_POST    
@login_required
def delete_student_qualification(request):
    delete_id = request.POST.get('delete_id')

    try:
        StudentQualification.objects.get(id=delete_id).delete()
    except StudentQualification.DoesNotExist:

        return JsonResponse(data={}, status=404)
    else:
        return JsonResponse({'success': True})
    





