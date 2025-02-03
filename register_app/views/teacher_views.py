from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from register_app.forms import TeacherForm
from register_app.models import Teacher 

@login_required
def teachers(request):
    context = {}
    return render(request, 'register_app/teachers/teachers.html', context)

@login_required
def teachers_headerbar(request):
    school=request.user.userprofile.school
    populated_periods = (list(
        school.periods
        .filter(teachers__isnull=False)
        .distinct().values_list('name', flat=True)
    ))
    if school.teachers.filter(periods__isnull=True).exists():
        populated_periods.append("Unassigned")
    context = {
        'periods': populated_periods,
        }
    return render(request, 'register_app/teachers/partials/teachers_headerbar.html', context)

@login_required
def teachers_table(request):
    school=request.user.userprofile.school
    populated_periods = (list(
        school.periods
        .filter(teachers__isnull=False)
        .distinct().values_list('name', flat=True)
    ))

    if school.teachers.filter(periods__isnull=True).exists():
        populated_periods.append("Unassigned")

    school.teachers
    context = {'teachers': school.teachers.all(), 'periods': populated_periods}
    return render(request, 'register_app/teachers/partials/teachers_table.html', context)

@login_required
def get_teacher_form(request, teacher_id):
    school=request.user.userprofile.school
    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        form = TeacherForm(initial={'school': school}, school=school)
    else:
        form = TeacherForm(instance=teacher, school=school)
    context = {'form': form}
    return render(request, 'register_app/teachers/partials/teacher_form.html', context)

@login_required
def save_teacher_form(request):
    teacher_id = request.POST.get('id')
    teacher = Teacher.objects.get(id=teacher_id) if teacher_id else None
    form = TeacherForm(request.POST, instance=teacher)
    if form.is_valid():
        form.save(commit=True)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@require_POST
@login_required
def delete_teacher(request):
    teacher_id = request.POST.get('delete-teacher_id')
    try:
        Teacher.objects.get(id=teacher_id).delete()
    except Teacher.DoesNotExist:
        return JsonResponse({}, status=404)
    else:
        return JsonResponse({})
    