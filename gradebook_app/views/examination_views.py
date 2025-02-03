from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from register_app.models import Student, Period, Enrollment
from register_app.models import StudentQualification
from gradebook_app.forms import QualificationExamResultForm, ComponentExamResultForm
from gradebook_app.models import QualificationExamResult, ComponentExamResult
from subject_app.models import Component
from django.db.models import Prefetch


@login_required
def examinations(request):
    context = {'url_headerbar': reverse('examinations-headerbar')}
    return render(request, 'gradebook_app/examinations/examinations.html', context)

@login_required
def examinations_headerbar(request):
    school = request.user.userprofile.school
    populated_periods = (list(
        school.periods
        .filter(enrollments__isnull=False)
        .distinct().values_list('name', 'id')
    ))

    period_options = []
    for period in populated_periods:
        print(period)
        period_options.append({
            'name': period[0],
            'url': reverse('examinations-table', kwargs={'period_id': period[1]}),
        })
    default_option = {
    'name': 'All',
    'url': reverse('examinations-table', kwargs={'period_id': 0}),
    }
    period_options.insert(0, default_option)

    context = {
        'period_options': period_options,
        'default_option': default_option
    }
    return render(request, 'gradebook_app/examinations/partials/examinations_headerbar.html', context)


@login_required
def examinations_table(request, period_id):
    students = Student.objects.filter(school=request.user.userprofile.school)
    context = {
        'students': students, 'period_id': period_id,
        'url_data': reverse('examinations-data', kwargs={'period_id': period_id})}
    return render(request, 'gradebook_app/examinations/partials/examinations_table.html', context)


@login_required
def examinations_data(request, period_id):
    data = []
    school = request.user.userprofile.school
    try:
        period = Period.objects.get(id=period_id)
    except Period.DoesNotExist:
        students = school.students.all().prefetch_related(
            'programmes__qualifications',
        )
        for student in students:
            setattr(student, 'enrollment', None)
    else:
        students = school.students.filter(periods=period).prefetch_related(
            Prefetch(
                'enrollments',
                queryset=Enrollment.objects.filter(period=period),
                to_attr='enrollment'
            ),
            'programmes__qualifications'
        )

    for student in students:
        enrollment = student.enrollment[0] if student.enrollment else None
        for programme in student.programmes.all():
            for qualification in programme.qualifications.all():
                rer = qualification.representative_exam_result()
                data.append({
                    'id': qualification.id,
                    'student': str(student),
                    'yeargroup': str(enrollment.yeargroup) if enrollment else "",
                    'qualification': str(qualification),
                    'programme': str(programme),
                    'grade': rer.grade if rer else "",
                    'year_series': f"{rer.get_series_display()} {rer.year}" if rer else "",
                    'hx_get': reverse('gradebook-examination-infocard', args=[qualification.id]),
                    'hx_target': '#examinations-infocard-container',
                    'hx_swap': 'innerHTML',
                })
    
    return JsonResponse({'data': data})


@login_required
def examination_infocard(request, pk):
    sq = StudentQualification.objects.get(pk=pk)
    if sq.qualification.modular:
        template = 'modular_examination_infocard.html' 
    else:
        template = 'linear_examination_infocard.html' 
    return render(
        request, 
        f"gradebook_app/examinations/partials/{template}",
        {'sq': sq}
    )

@login_required
def modular_qualification_exam_result_form(request, sq_id, qee_id):
    sq = StudentQualification.objects.get(id=sq_id)
    try:
        qee = QualificationExamResult.objects.get(id=qee_id)
    except QualificationExamResult.DoesNotExist:
        form = QualificationExamResultForm(
            prefix= "qer",
            qualification=sq.qualification, 
            initial={'student_qualification': sq}
        )
    else:
        form = QualificationExamResultForm(
            prefix= "qer",
            instance = qee, 
            qualification=sq.qualification
        )

    return render(
        request, 
        'gradebook_app/examinations/partials/modular_qualification_exam_result_form.html', 
        {'form': form, 'sq': sq}
    )


@require_POST
@login_required
def save_qualification_exam_result(request):
    qee_id = request.POST.get('qer-id')
    sq_id = request.POST.get('qer-student_qualification')
    sq = StudentQualification.objects.get(id=sq_id)
    qee = QualificationExamResult.objects.get(id=qee_id) if qee_id else None
    qer_form = QualificationExamResultForm(
        request.POST, 
        prefix= "qer",
        instance=qee, 
        qualification=sq.qualification
    )
    if qer_form.is_valid():
        qer_form.save(commit=True)
        return JsonResponse({'success': True})
    
    else:
        errors = {field: error[0] for field, error in qer_form.errors.items()}
        error_message = next(iter(errors.values()))
        return JsonResponse({"success": False, "error_message": error_message})
    

@login_required
def component_exam_result_form(request, sq_id, component_id, cee_id):
    sq = StudentQualification.objects.get(id=sq_id)
    component = Component.objects.get(id=component_id)
    try:
        cee = ComponentExamResult.objects.get(id=cee_id)
    except ComponentExamResult.DoesNotExist:
        form = ComponentExamResultForm(
            prefix= "cer",
            component=component, 
            initial={'student_qualification': sq, 'component': component}
        )
    else:
        form = ComponentExamResultForm(
            prefix= "cer",
            instance = cee, 
            component=component
        )

    return render(
        request, 
        'gradebook_app/examinations/partials/component_exam_result_form.html', 
        {'form': form, 'sq': sq, 'component': component}
    )


@require_POST
@login_required
def delete_qualification_exam_result(request):
    qer_id = request.POST.get('delete-qer-id')
    try:
        QualificationExamResult.objects.get(id=qer_id).delete()
    except:
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})
    

@require_POST
@login_required
def save_component_exam_result(request):
    cer_id = request.POST.get('cer-id')
    sq_id = request.POST.get('cer-student_qualification')
    component_id = request.POST.get('cer-component')
    component = Component.objects.get(id=component_id)
    sq = StudentQualification.objects.get(id=sq_id)
    cer = ComponentExamResult.objects.get(id=cer_id) if cer_id else None
    cer_form = ComponentExamResultForm(
        request.POST, 
        prefix= "cer",
        instance=cer, 
        component=component
    )
    if cer_form.is_valid():
        cer_form.save(commit=True)
        return JsonResponse({'success': True})
    
    else:
        errors = {field: error[0] for field, error in cer_form.errors.items()}
        error_message = next(iter(errors.values()))
        return JsonResponse({"success": False, "error_message": error_message})

@require_POST
@login_required
def delete_component_exam_result(request):
    cer_id = request.POST.get('delete-cer-id')
    try:
        ComponentExamResult.objects.get(id=cer_id).delete()
    except ComponentExamResult.DoesNotExist:
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})
    


@login_required
def linear_qualification_exam_result_form(request, sq_id, qer_id):
    sq = StudentQualification.objects.get(id=sq_id)
    lqer = QualificationExamResult.objects.filter(id=qer_id).first()
    qualification_form = QualificationExamResultForm(
        prefix= "lqer",
        qualification=sq.qualification, 
        instance = lqer,
        initial={'student_qualification': sq}
    )
        
    formset = []
    components = sq.qualification.components.all()
    for index, component in enumerate(components, start=1):
        lcer = ComponentExamResult.objects.filter(component=component, qualification_entry=lqer).first()
        lcer_form = ComponentExamResultForm(
            prefix= f"lcer-{index}",
            component=component, 
            instance = lcer,
            initial={
                'student_qualification': sq, 
                'component': component,
                'undertaken': False if (not lcer and lqer) else True,
            }
        )
        formset.append(lcer_form)
    component_formset =  zip(range(1, sq.qualification.components.count()+1), components, formset)
    
    return render(
        request, 
        'gradebook_app/examinations/partials/linear_qualification_exam_result_form.html', 
        {
            'qualification_form': qualification_form, 
            'sq': sq, 
            'component_formset': component_formset
        }
    )


@require_POST
@login_required
def save_linear_qualification_exam_result(request):
    qer_id = request.POST.get('lqer-id')
    sq_id = request.POST.get('lqer-student_qualification')
    sq = StudentQualification.objects.get(id=sq_id)
    lqer = QualificationExamResult.objects.get(id=qer_id) if qer_id else None
    lqer_form = QualificationExamResultForm(
        request.POST, 
        prefix= "lqer",
        instance=lqer, 
        qualification=sq.qualification
    )
    
    if lqer_form.is_valid():
        lqer = lqer_form.save(commit=False)
    else:
        errors = {field: error[0] for field, error in lqer_form.errors.items()}
        error_message = next(iter(errors.values()))
        return JsonResponse({"success": False, "error_message": error_message})

    components = sq.qualification.components.all()
    post_data = request.POST.copy() 
    lcer_instances = []
    formset_is_valid = True
    for index, component in enumerate(components, start=1):
        lcer_id = request.POST.get(f"lcer-{index}-id")
        lcer = ComponentExamResult.objects.get(id=lcer_id) if lcer_id else None
        post_data[f"lcer-{index}-year"] = lqer.year
        post_data[f"lcer-{index}-series"] = lqer.series
        lcer_form = ComponentExamResultForm(
            post_data, 
            prefix= f"lcer-{index}",
            instance=lcer, 
            component=component,
        )
        # Here could remove is_valid is valid given that we dont care about the form errors if form fails
        if lcer_form.is_valid():
            if not lcer_form.cleaned_data['undertaken']:
                if lcer:
                    lcer.delete()
            else:
                lcer = lcer_form.save(commit=False)
                lcer.qualification_entry = lqer 
                if not lcer.available:
                    lcer.grade = "n/a"
                    lcer.mark = None
                    lcer.is_final = False
                lcer_instances.append(lcer)
        else:
            formset_is_valid = False
 
    if formset_is_valid:    
        lqer.save()
        for lcer in lcer_instances:
            lcer.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False}, status=400)