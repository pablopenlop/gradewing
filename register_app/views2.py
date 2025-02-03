from django.shortcuts import render, redirect, get_object_or_404
from .forms import PeriodForm
from .forms import StudentForm, EnrollmentForm

from .forms import TeacherForm
from .forms import CourseForm
from .models import Period 
from .models import Student, Enrollment, Teacher, TeacherPeriod
from .models import Course
from subject_app.models import Qualification
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
import json
from django.template.loader import render_to_string
from .edusystem import QualificationSuite as QS
from django.contrib.auth.decorators import login_required

@login_required
def periods(request):
    periods = Period.objects.all().order_by('-start_month')
    if request.method == 'POST':
        pass
    form = PeriodForm(initial={'school': request.user.userprofile.school})
    return render(request, 'register_app/periods/periods.html', {'periods': periods, 'form': form})

def period_details(request, period_id):
    period = get_object_or_404(Period, pk=period_id)
    return render(request, 'register_app/periods/partials/period_details.html', {'period': period})

def programmes(request):
    periods = Period.objects.all().order_by('-start_month')
    if request.method == 'POST':
        pass
    form = PeriodForm()
    return render(request, 'register_app/programmes.html', {'periods': periods, 'form': form})




def students(request):
    period = Period.objects.filter(current=True).first()
    period_id=period.id
   
    if request.method == 'POST':
         period_id = request.POST.get("view-period")
         period = Period.objects.get(id = period_id)
 
    studentperiods = Enrollment.objects.filter(period_id=period_id)
    periods = Period.objects.all()
    context = {
        'studentperiods': studentperiods, 
        'periods': periods, 
        'this_period': period}
    return render(request, 'register_app/students/students.html', context)


def student_details(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'register_app/students/partials/student_details.html', {'student': student})





def teachers(request):
    period = Period.objects.filter(current=True).first()
    period_id=period.id
   
    if request.method == 'POST':
         period_id = request.POST.get("view-period")
         period = Period.objects.get(id = period_id)
 
    enrollments = TeacherPeriod.objects.filter(period_id=period_id)
    periods = Period.objects.all()
    context = {'enrollments': enrollments, 'periods': periods, 'this_period': period}
    return render(request, 'register_app/teachers.html', context)


def courses(request):
    period = Period.objects.last()
    period_id=period.id
   
    if request.method == 'POST':
         period_id = request.POST.get("view-period")
         period = Period.objects.get(id = period_id)
 
    courses = Course.objects.filter(period_id=period_id)
    periods = Period.objects.all()
    context = {'enrollments': courses, 'periods': periods, 'this_period': period}
    return render(request, 'register_app/courses.html', context)


@require_POST
def add_period(request):
    form = PeriodForm(request.POST)
    if form.is_valid():
        print("success")
        form.save()
        messages.success(request, 'Acadmic Period added successfully!')
        return JsonResponse({'success': True, 'redirect': reverse('periods')}) 
    else:
        # Return the rendered HTML form with errors
        return JsonResponse({
            'success': False,
            'html': render_to_string('register_app/partials/add_period_form.html', 
            {'form': form}, 
            request=request)
        })
    
@require_POST
def set_current_period(request, period_id):
    periods = Period.objects.all().order_by('-start_month')
    current_period = Period.objects.get(id=period_id)
    current_period.current = True
    current_period.save()
    return render(request, 'register_app/partials/period_cards.html', {'periods': periods})
""" 
def add_student(request):
    if request.method == "POST":
        student_form = StudentForm(request.POST)
        period_formset = EnrollmentFormSet(request.POST)
        subject_formset = StudentQualificationFormSet(request.POST)

        if student_form.is_valid() and period_formset.is_valid() and subject_formset.is_valid():
            print("here")
            student = student_form.save()
            periods = period_formset.save(commit=False)
            for period in periods:
                period.student = student
                period.save()
            
            subjects = subject_formset.save(commit=False)
            for subject in subjects:
                subject.student = student
                subject.save()
            return redirect('students')  
    else:
        student_form = StudentForm()
        period_formset = EnrollmentFormSet()
        for form in period_formset.forms[1:]:
            form.fields['DELETE'].initial = True
        subject_formset = StudentQualificationFormSet()
        for form in subject_formset.forms[1:]:
            form.fields['DELETE'].initial = True
    context = {
        'form': student_form,
        'period_formset': period_formset,
        'periods_allowed': periods_allowed(period_formset.extra),
        'subject_formset': subject_formset,
        'subjects_allowed': subject_formset.extra,
    }
    return render(request, 'register_app/add_student.html', context)


def add_student2(request):
    if request.method == "POST":
        student_form = StudentForm(request.POST)
        period_formset = EnrollmentFormSet(request.POST)
        subject_formset = StudentQualificationFormSet(request.POST)

        if student_form.is_valid() and period_formset.is_valid() and subject_formset.is_valid():
            print("here")
            student = student_form.save()
            periods = period_formset.save(commit=False)
            for period in periods:
                period.student = student
                period.save()
            
            subjects = subject_formset.save(commit=False)
            for subject in subjects:
                subject.student = student
                subject.save()
            return redirect('students')  
    else:
        student_form = StudentForm()
        period_formset = EnrollmentFormSet()
        period_formset.extra = 1
        subject_formset = StudentQualificationFormSet()
        subject_formset.extra = 1
    context = {
        'form': student_form,
        'period_formset': period_formset,
        'periods_allowed': periods_allowed(period_formset.extra),
        'subject_formset': subject_formset,
        'subjects_allowed': subject_formset.extra,
    }
    return render(request, 'register_app/add2_student.html', context)
"""

@login_required
def add_student(request):
    return render(request, 'register_app/students/add_student.html')

@login_required
def get_student_form(request):
    student_id = request.GET.get('student-id')
    print(student_id)
    try:
        student = Student.objects.get(id=student_id)
        form = StudentForm(instance=student, initial={'id': student.id})
    except:
        form = StudentForm(initial={'school': request.user.userprofile.school})
        print("Fresh S form")
    return render(request, 'register_app/students/partials/student_form.html', {'form': form})

@require_POST
def save_student_details(request):
    student_id = request.POST.get('id')
    student = None
    if student_id:
        student = get_object_or_404(Student, id=student_id) if student_id else None
    if student:
        form = StudentForm(request.POST, instance=student)
    else:
        form = StudentForm(request.POST)
    
    if form.is_valid():
        student = form.save(commit=True)
        return JsonResponse({
            'success': True,
            'html': render_to_string(
                'register_app/students/partials/student_person_details.html', 
                {'student': student}, 
                request=request
            )
        })
    return JsonResponse({   
            'success': False,
            'html': render_to_string(
                'register_app/students/partials/student_form.html', 
                {'form': form}, 
                request=request
            )
        })

def get_studentperiod_form(request):
    sp_id = request.GET.get('period-id')
    student_id = request.GET.get('student-id')
    print(sp_id)
    student = Student.objects.get(id=student_id)
    try:
        sp = Enrollment.objects.get(id=sp_id)
    except:
        form = EnrollmentForm(initial={'student': student})
        print("fresh SP form")
    else:
        print(sp.programme)
        a = QS.choices_from_values(sp.programme)
        print(a)
        form = EnrollmentForm(
            instance=sp, 
            initial={'programme': a}
        )
        
    return render(
        request, 
        'register_app/students/partials/student_period_form.html',
        {'form': form}
    )


@require_POST
def save_student_period(request):

    sp_id = request.POST.get('id')
    print(sp_id)
    sp = None
    if sp_id:
        sp = get_object_or_404(Enrollment, id=sp_id) if sp_id else None
    if sp:
        form = EnrollmentForm(request.POST, instance=sp)
    else:
        form = EnrollmentForm(request.POST)
    
    if form.is_valid():
        sp = form.save(commit=True)
        return JsonResponse({
            'success': True,
            'html': render_to_string(
                'register_app/students/partials/student_period_card.html', 
                {'period': sp}, 
                request=request
            )
        })
    return JsonResponse({   
            'success': False,
            'html': render_to_string(
                'register_app/students/partials/student_period_form.html', 
                {'form': form}, 
                request=request
            )
        })





def periods_allowed(max_count: int) -> int:
    period_count = Period.objects.count()
    return min(period_count, max_count)

""" 
def add_teacher(request):
    if request.method == "POST":
        teacher_form = TeacherForm(request.POST)
        period_formset = TeacherPeriodFormSet(request.POST)
        print(len(period_formset))
        if teacher_form.is_valid() and period_formset.is_valid():
            teacher = teacher_form.save()
            #periods = period_formset.save(commit=False)
            print(periods)
            for index, form in enumerate(period_formset):
                if form.cleaned_data.get('DELETE'):
                    print(index, form.cleaned_data.get('DELETE'))
                    continue
                period = form.save(commit=False)
                period.teacher = teacher
                period.save()
                print(index, form.cleaned_data.get('subject_areas'))
                period.subject_areas.set(form.cleaned_data.get('subject_areas'))
                period.save()
            return redirect('teachers')  
    else:
        teacher_form = TeacherForm()
        period_formset = TeacherPeriodFormSet()
        for form in period_formset.forms[1:]:
            form.fields['DELETE'].initial = True
    context = {
        'form': teacher_form,
        'period_formset': period_formset,
        'periods_allowed': periods_allowed(period_formset.extra),
    }
    return render(request, 'register_app/add_teacher.html', context)
"""

def add_course(request):
    course_form = CourseForm()
    if request.method == "POST":
        course_form3 = CourseForm(request.POST)
        print(course_form3)
    context = {'form': course_form}
    return render(request, 'register_app/add_course.html', context)



def add_course_enrollments(request, period_id):
    students = Enrollment.objects.filter(period_id=period_id)
    teachers = TeacherPeriod.objects.exclude(period_id=period_id)
    enrollment_ids = teachers.values_list('id', flat=True)
    enrollment_ids = list(enrollment_ids)
    context = {'students': students, 'exclude_teacher_ids': enrollment_ids}
    return render(request, 'register_app/partials/add_course_enrollments_table.html', context)


@require_POST
def delete_period(request):
    id_value = request.POST.get('confirm-delete')
    print("id val", id_value)
    period = get_object_or_404(Period, id=id_value)
    period.delete()
    messages.add_message(request, messages.SUCCESS, 'Deletion of selected Period was successful!')
    return redirect('periods')

@require_POST
def delete_students(request):
    selected_ids = request.POST.get('students-action')
    print("selected ids", selected_ids)
    if selected_ids:
        id_list = selected_ids.split(',')
        Student.objects.filter(id__in=id_list).delete()
        messages.add_message(request, messages.SUCCESS, 'Deletion was successful!')
    return redirect('students')


@require_POST
def add_qualification_students(request):
    subject_id = request.POST.get('subject')  
    students_id_str = request.POST.get('students_id') 
    external = True if request.POST.get('external') else False
    print(external)

    # Convert the 'students_id' to a list of strings
    students_id_list = students_id_str.split(',')

    # Get the qualification object
    subject = Qualification.objects.get(id=subject_id)

    # Iterate over the list of student IDs
    for student_id in students_id_list:
        student = Student.objects.get(id=student_id)

        # Use update_or_create to either update the existing record or create a new one
        """ 
        StudentQualification.objects.update_or_create(
            student=student,
            subject=subject,
            defaults={'external': external} 
        )
        """
    students = Student.objects.filter(id__in=students_id_list)
    print(students)
    # Add a success message
    messages.success(request, 'Qualification added successfully!')
    messages_html = render_to_string('components/messages.html', {'messages': messages.get_messages(request)})

    return JsonResponse({
        'messages_html': messages_html,
        'student_id': 2
    })

@require_POST
def delete_courses(request):
    selected_ids = request.POST.get('confirm-delete', '')
    if selected_ids:
        id_list = selected_ids.split(',')
        Course.objects.filter(id__in=id_list).delete()
        messages.add_message(request, messages.SUCCESS, 'Deletion was successful!')
    return redirect('courses')

@require_POST
def delete_teachers(request):
    selected_ids = request.POST.get('confirm-delete', '')
    if selected_ids:
        id_list = selected_ids.split(',')
        Teacher.objects.filter(id__in=id_list).delete()
        messages.add_message(request, messages.SUCCESS, 'Deletion was successful!')
    return redirect('teachers')



def add_student_old(request):
    form = StudentForm(request.POST or None)
    message = form.added_message()
    if request.method == 'POST' and form.is_valid():
        form.save()
        form = StudentForm()
    return render(request, 'register_app/partials/add_student_form.html', 
        {'form': form, 'text': message, 'is_post': request.method == 'POST'})