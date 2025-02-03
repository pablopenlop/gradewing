from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from register_app.forms import TeachingClassForm, TeachingClassPreForm1, TeachingClassPreForm2
from register_app.models import TeachingClass 

@login_required
def classes(request):
    context = {}
    return render(request, 'register_app/classes/classes.html', context)

@login_required
def classes_headerbar(request):
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
    return render(request, 'register_app/classes/partials/classes_headerbar.html', context)

@login_required
def classes_table(request):
    school=request.user.userprofile.school
    populated_periods = (list(
        school.periods
        .filter(teachers__isnull=False)
        .distinct().values_list('name', flat=True)
    ))

    if school.teachers.filter(periods__isnull=True).exists():
        populated_periods.append("Unassigned")
    teaching_classes = TeachingClass.objects.filter(period__school=school)
    context = {'teaching_classes': teaching_classes, 'periods': populated_periods}
    return render(request, 'register_app/classes/partials/classes_table.html', context)

@login_required
def get_class_preform_1(request):
    school=request.user.userprofile.school
    form = TeachingClassPreForm1(school=school)
    context = {'form': form}
    return render(request, 'register_app/classes/partials/class_preform_1.html', context)

@login_required
@require_POST
def get_class_preform_2(request):
    prev_form = TeachingClassPreForm1(request.POST)
    if prev_form.is_valid(): 
        period = prev_form.cleaned_data['period']
        form = TeachingClassPreForm2(initial={'period': period}, period=period)
        context = {'form': form, 'period_name': period.__str__()}
        return render(request, 'register_app/classes/partials/class_preform_2.html', context)


@login_required
def get_class_form(request, class_id):
    if request.method=="POST":
        prev_form = TeachingClassPreForm2(request.POST)
        if prev_form.is_valid(): 
            period = prev_form.cleaned_data['period']
            qualification = prev_form.cleaned_data['qualification']
            form = TeachingClassForm(
                initial={'period': period, 'qualification': qualification}, 
                period=period, 
                qualification=qualification
                )
    else:
        teaching_class = TeachingClass.objects.get(id=class_id)
        period=teaching_class.period
        qualification=teaching_class.qualification
        form = TeachingClassForm(
            instance=teaching_class,
            period=period, 
            qualification=qualification
            )
        
    context = {
        'form': form, 
        'period_name': period.__str__(), 
        'qualification_name': qualification.__str__()
        }
    return render(request, 'register_app/classes/partials/class_form.html', context)
    
    
@login_required
@require_POST
def save_class_form(request):
    class_id = request.POST.get('id')
    teaching_class = TeachingClass.objects.get(id=class_id) if class_id else None
    form = TeachingClassForm(request.POST, instance=teaching_class)
    if form.is_valid():
        form.save(commit=True)
        return JsonResponse({'success': True})
    errors = {field: error[0] for field, error in form.errors.items()}
    error_message = next(iter(errors.values()))
    return JsonResponse({"success": False, "error_message": error_message})


@require_POST
@login_required
def delete_class(request):
    class_id = request.POST.get('delete-class_id')
    try:
        TeachingClass.objects.get(id=class_id).delete()
    except TeachingClass.DoesNotExist:
        return JsonResponse({}, status=404)
    else:
        return JsonResponse({})
    
    
    