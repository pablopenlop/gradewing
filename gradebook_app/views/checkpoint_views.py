from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from register_app.models import Checkpoint
from gradebook_app.models import CheckpointEntry
from django.db.models import Prefetch
from choices.checkpoints import CheckpointFieldKind
from gradebook_app.forms import GradeEntryForm, CategoricalEntryForm
from choices.grading import Gradeset

@login_required
def checkpoints(request):
    context = {'url_headerbar': reverse('gradebook-checkpoints-headerbar')}
    return render(request, 'gradebook_app/checkpoints/checkpoints.html', context)


@login_required
def checkpoints_headerbar(request):
    school=request.user.userprofile.school
    populated_periods = (list(
        school.periods
        .filter(checkpoints__isnull=False)
        .distinct().values_list('name', flat=True)
    ))
    context = {
        'periods': populated_periods,
        'url_table': reverse('gradebook-checkpoints-table'),
        }
    return render(request, 'gradebook_app/checkpoints/partials/checkpoints_headerbar.html', context)

@login_required
def checkpoints_table(request):
    context = {'url_data': reverse('gradebook-checkpoints-data')}
    return render(request, 'gradebook_app/checkpoints/partials/checkpoints_table.html', context)

@login_required
def checkpoints_data(request):
    checkpoints_data = []
    school = request.user.userprofile.school
    checkpoints = Checkpoint.objects.filter(period__school=school).prefetch_related(
        'period',
        'yeargroups',
    )
    for checkpoint in checkpoints:
        checkpoints_data.append({
            'id': f"{checkpoint.id}",
            'name': checkpoint.name,
            'scope': checkpoint.get_scope_display(),
            'date': checkpoint.date.strftime("%B %-d, %Y"),
            'period': checkpoint.period.__str__(),
            'state': checkpoint.get_state_display(),
            'yeargroups': [
                yeargroup.__str__() for yeargroup in checkpoint.yeargroups.all()
            ],
            'url': reverse('gradebook-checkpoint-space', args=[checkpoint.id]),
        })

    return JsonResponse({'data': checkpoints_data})

@login_required
def checkpoint_space(request, checkpoint_id):
    checkpoint = Checkpoint.objects.get(id=checkpoint_id)
    context = {
        'checkpoint': checkpoint,
        'url_back': reverse('gradebook-checkpoints'),
        'url_table': reverse('gradebook-checkpoint-space-table', args=[checkpoint.id])
    }
    return render(request, 'gradebook_app/checkpoints/checkpoint_space.html',context)

@login_required
def checkpoint_space_table(request, checkpoint_id):
    checkpoint = Checkpoint.objects.get(id=checkpoint_id)
    context = {
        'checkpoint': checkpoint,
        'url_data': reverse('gradebook-checkpoint-space-data', args=[checkpoint_id])
    }
    return render(request, 'gradebook_app/checkpoints/partials/checkpoint_space_table.html', context)

@login_required
def checkpoint_space_data(request, checkpoint_id):

    checkpoint = Checkpoint.objects.prefetch_related('checkpoint_yeargroups', 'checkpoint_fields').get(id=checkpoint_id)

    data = []

    for cpyg in checkpoint.checkpoint_yeargroups.all():

        for ce in cpyg.class_enrollments.all():
            # Base dictionary with fixed fields
            entry_data = {
                "id": ce.id,
                "student": str(ce),
                "teaching_class": str(ce.teaching_class),
                "class_yeargroup": str(ce.teaching_class.yeargroup),
                "teaching_class_id": ce.teaching_class.id,
                "teachers": ce.teaching_class.get_teachers_display(),
                "qualification": str(ce.teaching_class.qualification),
            }
            
            # Fetch related checkpoint entries for the current class enrollment
            entries = CheckpointEntry.objects.filter(
                class_enrollment_id=ce.id,
                checkpoint_field__in=checkpoint.checkpoint_fields.all()
            )

            # Dynamically add each entry's value to the dictionary.
            for entry in entries:
                entry_key = entry.checkpoint_field.name  
                entry_data[entry_key] = {
                    'id': entry.id, 
                    'value': entry.value(),
                    'url_form': reverse('gradebook-checkpoint-entry-form', args=[entry.id])}
            
            data.append(entry_data)

    return JsonResponse({"data": data})


@login_required
def checkpoint_entry_form(request, checkpoint_entry_id):
    entry = CheckpointEntry.objects.get(id=checkpoint_entry_id)
    
    match entry.checkpoint_field.kind:
        case CheckpointFieldKind.GRADE:
            form = GradeEntryForm(instance=entry)
            template = "checkpoint_grade_entry_form.html"
        case CheckpointFieldKind.CATEGORICAL:
            form = CategoricalEntryForm(instance=entry)
            template = "checkpoint_categorical_entry_form.html"
    form.action=reverse('gradebook-checkpoint-entry-save')
    form.form_id='checkpoint-entry-form'
    return render(
        request, 
        f'gradebook_app/checkpoints/partials/{template}',
        {'form': form}
    )

@require_POST
@login_required
def save_checkpoint_entry(request):
    entry_id = request.POST.get('id')
    entry = CheckpointEntry.objects.get(id=entry_id)
    match entry.checkpoint_field.kind:
        case CheckpointFieldKind.GRADE:
            form = GradeEntryForm(request.POST, instance=entry)
        case CheckpointFieldKind.CATEGORICAL:
            form = CategoricalEntryForm(request.POST, instance=entry)
    
    if form.is_valid():
        ce=form.save(commit=True)
        print("SAVED", ce.value())
        return JsonResponse({'success': True, 'data': ce.value()})
    else:
        return JsonResponse({'success': False})
