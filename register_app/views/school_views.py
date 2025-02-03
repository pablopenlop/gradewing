from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from register_app.models import YearGroup, Period
from django.db import IntegrityError

from choices import YearGroupSystem
from register_app.forms import YearGroupForm, PeriodForm, SchoolForm
from register_app.forms import AddStudentTagsForm, AddTeacherTagsForm 
from register_app.forms import StudentTagForm, TeacherTagForm
from register_app.visualizers import YearGroupPresetsVis
from register_app.models import StudentTag, TeacherTag

from shared.delete import DeleteForm

@login_required
def school(request):
    school=request.user.userprofile.school
    context = { 
        'school': school
    }
    return render(request, 'register_app/school/school.html', context)


@login_required
def school_card(request):
    school=request.user.userprofile.school
    context = { 
        'school': school, 
    }
    return render(request, 'register_app/school/partials/school_card.html', context)


@login_required
def school_form(request):
    school=request.user.userprofile.school
    form = SchoolForm(instance=school)
    context = {'form': form}
    return render(request, 'register_app/school/partials/school_form.html', context)


@require_POST
@login_required
def save_school(request):
    school=request.user.userprofile.school
    form = SchoolForm(request.POST, instance=school)
    print("here")
    if form.is_valid(): 
        form.save(commit=True)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({}, status=400)
    
    
@login_required
def yeargroups_card(request):
    school=request.user.userprofile.school
    context = { 
        'yearGroupPresets': YearGroupPresetsVis(), 
        'yeargroups': school.yeargroups.all(), 
        'school_system': school.yeargroup_system,
        'school_system_label': school.get_yeargroup_system_display,
    }
    return render(request, 'register_app/school/partials/yeargroups_card.html', context)


@login_required
def custom_yeargroup_form(request, yeargroup_id):
    yg = YearGroup.objects.get(id=yeargroup_id)
    context = { 
        'form': YearGroupForm(instance=yg), 'yeargroup': yg,
    }
    if request.method == "POST":
        form = YearGroupForm(request.POST, instance=yg)
        if form.is_valid():
            try:
                form.save(commit=True)
                return JsonResponse({'success': True})
            except IntegrityError:
                return JsonResponse({'success': False, 'error_message': 'A year group with this name already exists.'})
        else:
            return JsonResponse({'success': False}, status=404)
    return render(request, 'register_app/school/partials/yeargroup_form.html', context)

@require_POST
@login_required
def set_yeargroup_system(request):
    system = request.POST.get('system')
    school=request.user.userprofile.school
    if system in YearGroupSystem.values:
        school.yeargroup_system = system
        school.save()
    return yeargroups_card(request)


@login_required
def periods_card(request):
    school=request.user.userprofile.school
    periods = school.periods.all()
    context = {'periods': periods}
    return render(request, 'register_app/school/partials/periods_card.html', context)


@login_required
def get_period_form(request, period_id):
    school=request.user.userprofile.school
    try:
        period = Period.objects.get(id=period_id)
    except Period.DoesNotExist:
        form = PeriodForm(initial={'school': school})
    else:
        form = PeriodForm(instance=period)
    context = {'form': form}
    return render(request, 'register_app/school/partials/period_form.html', context)

@require_POST
@login_required
def save_period(request):
    period_id = request.POST.get('id')
    period = Period.objects.get(id=period_id) if period_id else None
    form = PeriodForm(request.POST, instance=period)
    if form.is_valid(): 
        form.save(commit=True)
        return JsonResponse({'success': True})
    else:
        errors = {field: error[0] for field, error in form.errors.items()}
        error_message = next(iter(errors.values()))
        return JsonResponse({"success": False, "error_message": error_message})
    
    
@login_required
def period_delete_form(request, period_id):
    context = {'form': DeleteForm(model=Period, delete_id=period_id)}
    return render(request, 'partials/delete_form.html', context)
    
@require_POST
@login_required
def delete_period(request):
    period_id = request.POST.get('delete_id')
    try:
        Period.objects.get(id=period_id).delete()
    except Period.DoesNotExist:
        return JsonResponse({}, status=404)
    else:
        return JsonResponse({})
    
@require_POST
@login_required
def set_current_period(request, period_id):
    try:
        current_period = Period.objects.get(id=period_id)
    except Period.DoesNotExist:
        return JsonResponse({}, status=404)
    else:
        current_period.current = True
        current_period.save()
        return periods_card(request)
    
@login_required
def get_tags_form(request, tag_type):
    if tag_type=="student":
        form = AddStudentTagsForm()
    else:
        form = AddTeacherTagsForm()
    context = {'form': form, 'tag_type': tag_type}
    return render(request, 'register_app/school/partials/tags_form.html', context)

@login_required
def get_tag_actions_form(request, tag_type, tag_id):
    tag_models = {
        "student": (StudentTag, StudentTagForm),
        "teacher": (TeacherTag, TeacherTagForm),
    }
    tag_model, tag_form = tag_models[tag_type]
    tag_instance = tag_model.objects.get(id=tag_id)
    form = tag_form(instance=tag_instance)
    context = {'form': form, 'tag_type': tag_type}
    return render(request, 'register_app/school/partials/tag_actions_form.html', context)


@login_required
def tags_card(request):
    school=request.user.userprofile.school
    context = {
        'student_tags': school.student_tags.all(),
        'teacher_tags': school.teacher_tags.all(),
        'tags_count': school.student_tags.count()+school.teacher_tags.count(),
        }
    return render(request, 'register_app/school/partials/tags_card.html', context)

@require_POST
@login_required
def add_tags(request, tag_type):
    school = request.user.userprofile.school
    tag_data = {
        "student": (AddStudentTagsForm, StudentTag),
        "teacher": (AddTeacherTagsForm, TeacherTag),
    }
    form_class, tag_model = tag_data[tag_type]
    form = form_class(request.POST)
    if form.is_valid():
        tags = form.cleaned_data['tags']
        print(tags)
        for tag in tags:
            tag_model.objects.get_or_create(name=tag, school=school)
        return JsonResponse({})
    print(form.errors)
    return JsonResponse({}, status=400)

@login_required
def add_tags3(request, tag_type):
    school = request.user.userprofile.school
    if tag_type=="student":
        form = AddStudentTagsForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            for tag in tags:
                StudentTag.objects.get_or_create(name=tag, school=school)
            return JsonResponse({})
        return JsonResponse({}, status=400)
    else:
        form = AddTeacherTagsForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            for tag in tags:
                TeacherTag.objects.get_or_create(name=tag, school=school)
            return JsonResponse({})
        return JsonResponse({}, status=400)


""" @require_POST
@login_required
def save_tag(request, tag_type):
    tag_id = request.POST.get('id')
    if tag_type=="student":
        tag = StudentTag.objects.get(id=tag_id)
        form = StudentTagForm(request.POST, instance=tag)
    elif tag_type=="teacher":
        tag = TeacherTag.objects.get(id=tag_id)
        form = TeacherTagForm(request.POST, instance=tag)
    print(form.errors)
    if form.is_valid():
        form.save(commit=True)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error_message': f"A {tag_type} tag with this name already exists."})
 """

@require_POST
@login_required
def save_tag(request, tag_type):
    tag_data = {
        "student": (StudentTag, StudentTagForm),
        "teacher": (TeacherTag, TeacherTagForm),
    }

    tag_model, tag_form = tag_data[tag_type]
    tag_id = request.POST.get('id')
    tag = tag_model.objects.get(id=tag_id)
    form = tag_form(request.POST, instance=tag)

    if form.is_valid():
        form.save(commit=True)
        return JsonResponse({'success': True})
    else:
        error_message = f"A {tag_type} tag with this name already exists."
        return JsonResponse({'success': False, 'error_message': error_message})


@login_required
def delete_tag_form(request, tag_type, tag_id):
    context={"tag_type": tag_type, "tag_id": tag_id,}
    return render(request, 'register_app/school/partials/tag_delete_form.html', context)

@login_required
def delete_tag(request):
    tag_models = {
        "student": StudentTag,
        "teacher": TeacherTag,
    }
    tag_id = request.POST.get('delete-tag_id')
    tag_type = request.POST.get('delete-tag_type')
    tag_model = tag_models[tag_type]
    print("AAAAAtag")
    try:
        tag_model.objects.get(id=tag_id).delete()
    except tag_model.DoesNotExist:
        print("fack")
        return JsonResponse({}, status=404)
    else:
        return JsonResponse({})