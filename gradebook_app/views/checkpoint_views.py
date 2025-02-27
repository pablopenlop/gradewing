from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from register_app.models import Checkpoint
from gradebook_app.models import CheckpointEntry
from choices.checkpoints import CheckpointFieldKind, CheckpointScope
from gradebook_app.forms import (
    GradeEntryForm, GradeMarkEntryForm, CategoricalEntryForm, 
    MarkEntryForm, CommentEntryForm, MockEntryPreForm, MockEntryForm
)
from shared.utils.form_utils import limits_from_validators
import time
from django.db import connection

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
        checkpoint.progress()
        checkpoints_data.append({
            'id': f"{checkpoint.id}",
            'name': checkpoint.name,
            'scope': checkpoint.get_scope_display(),
            'date': checkpoint.date.strftime("%B %-d, %Y"),
            'period': checkpoint.period.__str__(),
            'state': checkpoint.get_state_display(),
            'yeargroups': ", ".join(map(str, checkpoint.yeargroups.all())),
            'progress': checkpoint.progress(),
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
    scope = Checkpoint.objects.get(id=checkpoint_id).scope
    context = {
        'scope': scope,
        'url_data': reverse('gradebook-checkpoint-space-data', args=[checkpoint_id]),
    }
    return render(request, 'gradebook_app/checkpoints/partials/checkpoint_space_table.html', context)

@login_required
def checkpoint_space_data(request, checkpoint_id):
    scope = Checkpoint.objects.get(id=checkpoint_id).scope
    match scope:
        case CheckpointScope.SUBJECT_BENCHMARK:
            return subject_benchmark_data(checkpoint_id)
        case CheckpointScope.CLASS_LANDMARK:
            return class_landmark_data(checkpoint_id)
        case CheckpointScope.GENERAL_BENCHMARK:
            return general_benchmark_data(checkpoint_id)

def general_benchmark_data(checkpoint_id):
    checkpoint = Checkpoint.objects.prefetch_related(
        'checkpoint_yeargroups', 
        'checkpoint_yeargroups__enrollments', 
        'checkpoint_yeargroups__enrollments__student', 
        'checkpoint_yeargroups__enrollments__student__tags', 
        'checkpoint_yeargroups__enrollments__yeargroup__school', 
        'checkpoint_yeargroups__enrollments__tags', 
        'checkpoint_yeargroups__enrollments__checkpoint_entries', 
        'checkpoint_yeargroups__enrollments__checkpoint_entries__checkpoint_field', 
        'checkpoint_yeargroups__enrollments__student__programmes',
        'checkpoint_yeargroups__enrollments__student__programmes__qualifications__enrollments',  
        'checkpoint_fields',
        ).get(id=checkpoint_id)
    data = []
    for cpyg in checkpoint.checkpoint_yeargroups.all():
        for enr in cpyg.enrollments.all():
            entry_data = {
                "student": str(enr.student),
                "yeargroup": str(enr.yeargroup),
                "tags": enr.tags_as_list(),
                "programme": ", ".join(enr.programmes_with_count()),
            }
            entries = [
                entry for entry in enr.checkpoint_entries.all()
                if entry.checkpoint_field in checkpoint.checkpoint_fields.all()
            ]
        
            for entry in entries:
                entry_key = entry.checkpoint_field.name  
                data_bs_target, hx_target = entry.bs_hx_targets()
                entry_data[entry_key] = {
                    'id': entry.id, 
                    'value': entry.value(),
                    'is_excluded': entry.is_excluded,
                    'data_bs_target': data_bs_target,
                    'hx_target': hx_target,
                    'url_form': reverse('gradebook-checkpoint-entry-form', args=[entry.id])}
            
            data.append(entry_data)
    print("Queries:", len(connection.queries))
    return JsonResponse({"data": data})
   

def subject_benchmark_data(checkpoint_id):
    start_time = time.time()
    checkpoint = Checkpoint.objects.prefetch_related(
        'checkpoint_yeargroups',
        'checkpoint_yeargroups__enrollment_qualifications__enrollment', 
        'checkpoint_yeargroups__enrollment_qualifications__enrollment__yeargroup',
        'checkpoint_yeargroups__enrollment_qualifications__enrollment__student', 
        'checkpoint_yeargroups__enrollment_qualifications__student_qualification__qualification', 
        'checkpoint_yeargroups__enrollment_qualifications__checkpoint_entries', 
        'checkpoint_yeargroups__enrollment_qualifications__checkpoint_entries__component', 
        'checkpoint_yeargroups__enrollment_qualifications__checkpoint_entries__checkpoint_field', 
        'checkpoint_fields'
    ).get(id=checkpoint_id)
    data = []
    print(f"Elapsed time (before processing): {time.time() - start_time:.6f} seconds")
    for cpyg in checkpoint.checkpoint_yeargroups.all():
        for eq in cpyg.enrollment_qualifications.all():
            entry_data = {
                "student": str(eq.enrollment.student),
                "yeargroup": str(eq.enrollment.yeargroup),
                "qualification": str(eq.student_qualification.qualification),
            }
            
            entries = [
                entry for entry in eq.checkpoint_entries.all()
                if entry.checkpoint_field in checkpoint.checkpoint_fields.all()
            ]
 
            entry_data.update({
                entry.checkpoint_field.name: {
                    'id': entry.id,
                    'value': entry.value(),
                    'is_excluded': entry.is_excluded,
                    'data_bs_target': entry.bs_hx_targets()[0],
                    'hx_target': entry.bs_hx_targets()[1],
                    'url_form': (
                        reverse('gradebook-checkpoint-entry-componentless')
                        if entry.is_always_excluded()
                        else reverse('gradebook-checkpoint-entry-form', args=[entry.id])
                    ),
                }
                for entry in entries
            })
            data.append(entry_data)

    elapsed_time = time.time() - start_time
    print("Queries:", len(connection.queries))
    print(f"Elapsed time (after processing): {elapsed_time:.6f} seconds")
    return JsonResponse({"data": data})

                   
def class_landmark_data(checkpoint_id):
    start_time = time.time()
    checkpoint = Checkpoint.objects.prefetch_related(
        'checkpoint_yeargroups__class_enrollments__enrollment_qualification__enrollment__student', 
        'checkpoint_yeargroups__class_enrollments__teaching_class__teachers', 
        'checkpoint_yeargroups__class_enrollments__teaching_class__yeargroup__school', 
        'checkpoint_yeargroups', 
        'checkpoint_yeargroups__class_enrollments', 
        'checkpoint_yeargroups__class_enrollments__teaching_class__qualification', 
        'checkpoint_yeargroups__class_enrollments__teaching_class', 
        'checkpoint_yeargroups__class_enrollments__checkpoint_entries', 
        'checkpoint_yeargroups__class_enrollments__checkpoint_entries__checkpoint_field', 
        'checkpoint_yeargroups__class_enrollments__checkpoint_entries__class_enrollment__enrollment_qualification__student_qualification__qualification',
        'checkpoint_yeargroups__class_enrollments__checkpoint_entries__class_enrollment__enrollment_qualification__student_qualification__qualification__components',

        'checkpoint_fields'
        ).get(id=checkpoint_id)

    data = []
    print(f"Elapsed time (before processing): {time.time() - start_time:.6f} seconds")
    for cpyg in checkpoint.checkpoint_yeargroups.all():
        for ce in cpyg.class_enrollments.all():
            entry_data = {
                "student": str(ce),
                "teaching_class": str(ce.teaching_class),
                "class_yeargroup": str(ce.teaching_class.yeargroup),
                "teachers": ce.teaching_class.get_teachers_display(),
                "qualification": str(ce.teaching_class.qualification),
            }
            entries = [
                entry for entry in ce.checkpoint_entries.all()
                if entry.checkpoint_field in checkpoint.checkpoint_fields.all()
            ]
            for entry in entries:
                entry_key = entry.checkpoint_field.name  
                data_bs_target, hx_target = entry.bs_hx_targets()
                entry_data[entry_key] = {
                    'id': entry.id, 
                    'value': entry.value(),
                    'data_bs_target': data_bs_target,
                    'hx_target': hx_target,
                    'is_excluded': entry.is_excluded,
                    'url_form': (
                        reverse('gradebook-checkpoint-entry-componentless')
                        if entry.is_always_excluded()
                        else reverse('gradebook-checkpoint-entry-form', args=[entry.id])
                    ),
                    }           
            data.append(entry_data)        
    print("Queries:", len(connection.queries))
    print(f"Elapsed time (after processing): {time.time() - start_time:.6f} seconds")
    return JsonResponse({"data": data})



@login_required
def checkpoint_entry_componentless(request):
    return render(
        request, 
        'gradebook_app/checkpoints/partials/checkpoint_mock_entry_componentless.html',
        {}
    )
    
@login_required
def checkpoint_entry_form(request, checkpoint_entry_id):
    entry = CheckpointEntry.objects.get(id=checkpoint_entry_id)
    is_preform = False
    match entry.checkpoint_field.kind:
        case CheckpointFieldKind.GRADE:
            qualification = entry.qualification()
            if qualification.mark_required:
                form = GradeMarkEntryForm(instance=entry)
                template = "checkpoint_grade_mark_entry_form.html"
            else:
                form = GradeEntryForm(instance=entry)
                template = "checkpoint_grade_entry_form.html"    
        case CheckpointFieldKind.CATEGORICAL:
            form = CategoricalEntryForm(instance=entry)
            template = "checkpoint_categorical_entry_form.html"
        case CheckpointFieldKind.MARK | CheckpointFieldKind.PERCENTAGE:
            form = MarkEntryForm(instance=entry)
            template = "checkpoint_mark_entry_form.html"
        case CheckpointFieldKind.MOCK:
            if entry.component:
                form = MockEntryForm(instance=entry)
                template = "checkpoint_mock_entry_form.html"
            else:
                form = MockEntryPreForm(instance=entry)
                template = "checkpoint_mock_entry_preform.html" 
                is_preform = True
        case CheckpointFieldKind.COMMENT:
            form = CommentEntryForm(instance=entry)
            comment_field = CheckpointEntry._meta.get_field('comment')
            _, form.max_comment_length = limits_from_validators(comment_field)
            template = "checkpoint_comment_entry_form.html"
    
    form.action=reverse('gradebook-checkpoint-entry-save')
    form.form_id='checkpoint-entry-form'

    return render(
        request, 
        f'gradebook_app/checkpoints/partials/{template}',
        {'form': form, 'is_preform': is_preform}
    )

@require_POST
@login_required
def save_checkpoint_entry(request):
    entry_id = request.POST.get('id')
    action = request.POST.get('action')
    if action == "clear-entry":
        return clear_checkpoint_entry(entry_id)
    elif action == "exclude-entry":
        return exclude_checkpoint_entry(entry_id)
    else:
        return update_checkpoint_entry(request, entry_id)
    

def update_checkpoint_entry(request, entry_id):
    entry = CheckpointEntry.objects.get(id=entry_id)
    match entry.checkpoint_field.kind:
        case CheckpointFieldKind.GRADE:
            qualification = entry.qualification()
            if qualification.mark_required:
                form = GradeMarkEntryForm(request.POST, instance=entry)
            else:
                form = GradeEntryForm(request.POST, instance=entry)
        case CheckpointFieldKind.CATEGORICAL:
            form = CategoricalEntryForm(request.POST, instance=entry)
        case CheckpointFieldKind.MARK | CheckpointFieldKind.PERCENTAGE:
            form = MarkEntryForm(request.POST, instance=entry)
        case CheckpointFieldKind.COMMENT:
            form = CommentEntryForm(request.POST, instance=entry)
        case CheckpointFieldKind.MOCK:
            if entry.component:
                form = MockEntryForm(request.POST, instance=entry)
            else:
                form = MockEntryPreForm(request.POST, instance=entry)
                if form.is_valid():
                    form.save()
                    return checkpoint_entry_form(request, entry_id)
                
    if form.is_valid():
        ce=form.save(commit=True)
        ce.is_excluded = False
        ce.is_completed = True
        ce.save()
        return JsonResponse({'success': True, 'value': ce.value(), 'is_excluded': False})
    else:
        return JsonResponse({'success': False})
    

def clear_checkpoint_entry(entry_id):
    entry = CheckpointEntry.objects.get(id=entry_id)
    entry.clear()
    entry.is_excluded = False
    entry.component = None
    entry.is_completed = False
    entry.save()
    return JsonResponse({'success': True, 'value': None, 'is_excluded': False})


def exclude_checkpoint_entry(entry_id):
    entry = CheckpointEntry.objects.get(id=entry_id)
    entry.clear()
    entry.is_excluded = True
    entry.component = None
    entry.is_completed = False
    entry.save()
    return JsonResponse({'success': True, 'value': None, 'is_excluded': True})