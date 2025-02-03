from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from gradebook_app.models import CheckpointEntry

from register_app.forms import (
    CheckpointPreForm1, CheckpointPreForm2, CheckpointFieldForm, 
    CheckpointYeargroupForm
)
from register_app.models import (
    EnrollmentQualification, ClassEnrollment, Enrollment,
    Checkpoint, CheckpointField, CheckpointYearGroup
)
from choices.checkpoints import CheckpointScope, CheckpointFieldKind, CheckpointState
import json
from shared.delete import DeleteForm
from django.db.models import Prefetch


@login_required
def checkpoints(request):
    context = {}
    return render(request, 'register_app/checkpoints/checkpoints.html', context)

@login_required
def checkpoints_headerbar(request):
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
    return render(
        request, 
        'register_app/checkpoints/partials/checkpoints_headerbar.html', 
        context
    )

@login_required
def checkpoints_table(request):
    school=request.user.userprofile.school
    populated_periods = (list(
        school.periods
        .filter(teachers__isnull=False)
        .distinct().values_list('name', flat=True)
    ))

    if school.teachers.filter(periods__isnull=True).exists():
        populated_periods.append("Unassigned")
    checkpoints = Checkpoint.objects.filter(period__school=school)
    context = {'checkpoints': checkpoints, 'periods': populated_periods}
    return render(request, 'register_app/checkpoints/partials/checkpoints_table.html', context)

@login_required
def get_checkpoint_preform_1(request):
    school=request.user.userprofile.school
    form = CheckpointPreForm1(school=school)
    context = {'form': form}
    return render(request, 'register_app/checkpoints/partials/checkpoint_preform_1.html', context)

@login_required
@require_POST
def get_checkpoint_preform_2(request):
    school=request.user.userprofile.school
    prev_form = CheckpointPreForm1(request.POST)
    if prev_form.is_valid(): 
        period = prev_form.cleaned_data['period']
        scope = prev_form.cleaned_data['scope']
        form = CheckpointPreForm2(initial={'period': period, 'scope': scope}, school=school)
        context = {'form': form, 'period_name': period.__str__(), 'scope_name': CheckpointScope(scope).label }
        return render(request, 'register_app/checkpoints/partials/checkpoint_preform_2.html', context)


@login_required
def get_checkpoint_form(request, checkpoint_id):
    school=request.user.userprofile.school
    checkpoint = Checkpoint.objects.get(id=checkpoint_id)
    form = CheckpointPreForm2(instance=checkpoint, initial={'period': checkpoint.period}, school=school)
    context = {
        'form': form, 
        'period_name': checkpoint.period.__str__(), 
        'scope_name': CheckpointScope(checkpoint.scope).label 
    }
    return render(request, 'register_app/checkpoints/partials/checkpoint_preform_2.html', context)


@login_required
def checkpoint_delete_form(request, checkpoint_id):
    context = {
        'form': DeleteForm(model=Checkpoint, delete_id=checkpoint_id), 
    }
    return render(request, 'partials/delete_form.html', context)


@login_required
@require_POST
def save_checkpoint(request):
    cp_id = request.POST.get('id')
    cp = Checkpoint.objects.get(id=cp_id) if cp_id else None
    form = CheckpointPreForm2(request.POST, instance=cp)
    if form.is_valid():
        cp=form.save(commit=True)
        return JsonResponse({
            'success': True, 
             'redirect_url': reverse('checkpoint-editor', kwargs={'checkpoint_id': cp.id})
            })
    else:
        errors = {field: error[0] for field, error in form.errors.items()}
        error_message = next(iter(errors.values()))
        return JsonResponse({"success": False, "error_message": error_message})



@require_POST
@login_required
def delete_checkpoint(request):
    checkpoint_id = request.POST.get('delete_id')
    print(checkpoint_id)
    try:
        Checkpoint.objects.get(id=checkpoint_id).delete()
    except Checkpoint.DoesNotExist:
        return JsonResponse({}, status=404)
    else:
        return JsonResponse({}) 
    
    

@login_required
def checkpoint_fields_table(request, checkpoint_id):
    context = {'checkpoint': Checkpoint.objects.get(id=checkpoint_id)}
    return render(request, 'register_app/checkpoints/partials/checkpoint_fields_table.html', context)
    

@login_required
def checkpoint_editor(request, checkpoint_id):
    context = {'checkpoint_id': Checkpoint.objects.get(id=checkpoint_id).id}
    return render(request, 'register_app/checkpoints/checkpoint_editor.html', context)


@login_required
def checkpoint_editor_details_card(request, checkpoint_id):
    # add checkpointstates
    context = {
        'checkpoint': Checkpoint.objects.get(id=checkpoint_id),
        'states': CheckpointState.detailed_choices()}
    return render(request, 'register_app/checkpoints/partials/checkpoint_details_card.html', context)

@login_required
def checkpoint_editor_fields_card(request, checkpoint_id):
    context = {
        'checkpoint': Checkpoint.objects.get(id=checkpoint_id)}
    return render(request, 'register_app/checkpoints/partials/checkpoint_fields_card.html', context)

@login_required
def checkpoint_field_form(request, checkpoint_id, checkpointfield_id, field_kind=None):
    cp= Checkpoint.objects.get(id=checkpoint_id)
    try:
        cpfield = CheckpointField.objects.get(id=checkpointfield_id)
    except CheckpointField.DoesNotExist:
        form = CheckpointFieldForm(initial={
            'checkpoint': cp,
            'kind': field_kind
            })
    else:
        form = CheckpointFieldForm(instance=cpfield)
    context = {'form': form ,'kind_label': CheckpointFieldKind(field_kind).label }
    return render(request, 'register_app/checkpoints/partials/checkpoint_field_form.html', context)



@login_required
@require_POST
def save_checkpoint_field(request):
    cpf_id = request.POST.get('id')
    cpf = CheckpointField.objects.get(id=cpf_id) if cpf_id else None
    form = CheckpointFieldForm(request.POST, instance=cpf)
    
    if not form.is_valid():
        errors = {field: error[0] for field, error in form.errors.items()}
        error_message = next(iter(errors.values()))
        return JsonResponse({'success': False, 'error_message': error_message})
    
    cp_field=form.save()
    
    if cpf_id:
        return JsonResponse({'success': True})
    
    cp_yeargroups = cp_field.checkpoint.checkpoint_yeargroups.all()
    for cpyg in cp_yeargroups:
        assign_checkpoints(
            cpyg_id = cpyg.id, 
            target_ids=cpyg.assigned_target_ids(), 
            checkpoint_field_id=cp_field.id
        )
    print("ADDED")
    return JsonResponse({'success': True})
    
    




@require_POST
@login_required
def delete_checkpoint_field(request):
    field_id = request.POST.get('delete-field_id')
    try:
        cpf = CheckpointField.objects.get(id=field_id)
    except CheckpointField.DoesNotExist:
        return JsonResponse({}, status=404)
    else:
        cp = cpf.checkpoint
        cpf.delete()
        cp.reorder_fields()
        return JsonResponse({}) 

@require_POST
@login_required
def reorder_checkpoint_field(request):
    data = json.loads(request.body)
    checkpoint_id = data.get('checkpoint_id')
    reorder_data = data.get('reorder', [])

    # Fetch the relevant checkpoint
    checkpoint = Checkpoint.objects.get(id=checkpoint_id)

    # Reorder the CheckpointField objects
    cpflist = [
        CheckpointField.objects.get(checkpoint=checkpoint, index=row['old_position'])
        for row in reorder_data
    ]
    for row, cpf in zip(reorder_data, cpflist):
        cpf.index = row['new_position']
        cpf.save()

    return JsonResponse({'status': 'success'})



@login_required
def checkpoint_editor_targets_card(request, checkpoint_id):
    # Fetch Checkpoint and its period_id in one go
    checkpoint = (
        Checkpoint.objects
        .only('id', 'period_id')
        .get(id=checkpoint_id)
    )

    # Prefetch only CheckpointYearGroups related to this checkpoint
    checkpoint_yeargroups_qs = (
        CheckpointYearGroup.objects
        .filter(checkpoint_id=checkpoint_id)
        .only('id', 'checkpoint_id', 'yeargroup_id')
    )
    # Fetch checkpoint with optimized prefetching
    checkpoint = (
        Checkpoint.objects
        .filter(id=checkpoint_id)
        .prefetch_related(
            Prefetch('checkpoint_yeargroups', queryset=checkpoint_yeargroups_qs),
        )
        .only('id')
        .get()
    )
    checkpoint.url_form = reverse('checkpoint-yeargroup-form', args=[checkpoint_id])

    for checkpoint_yeargroup in checkpoint.checkpoint_yeargroups.all():
        checkpoint_yeargroup.url_deleteform = reverse(
            'checkpoint-yeargroup-delete-form',
            args=[checkpoint_yeargroup.id]
        )
        checkpoint_yeargroup.url_table = reverse(
            'checkpoint-yeargroup-targets-table',
            kwargs={'cpyg_id': checkpoint_yeargroup.id} 
        )

    context = {'checkpoint': checkpoint}
    return render(request, 'register_app/checkpoints/partials/checkpoint_targets_card.html', context)



@login_required
def checkpoint_yeargroup_form(request, checkpoint_id):
    cp = Checkpoint.objects.get(id=checkpoint_id)
    form = CheckpointYeargroupForm(instance=cp)
    form = CheckpointYeargroupForm(initial={'checkpoint': cp}, checkpoint=cp)
    form.action = reverse('checkpoint-yeargroup-save')
    form.form_id= "checkpoint-yeargroup-form"
    context = {'form': form }
    return render(request, 'register_app/checkpoints/partials/checkpoint_target_form.html', context)


@login_required
def checkpoint_yeargroup_delete_form(request, cpyg_id):
    context = {'form': DeleteForm(model=CheckpointYearGroup, delete_id=cpyg_id)}
    return render(request, 'partials/delete_form.html', context)

@login_required
@require_POST
def save_checkpoint_yeargroup(request):
    form = CheckpointYeargroupForm(request.POST)
    if form.is_valid():
        cpyg=form.save()
        assign_checkpoints(cpyg_id=cpyg.id, target_ids=cpyg.target_ids())
        return JsonResponse({})
    else:
        return JsonResponse({}, status=404)

@require_POST
@login_required
def delete_checkpoint_yeargroup(request):
    cpyg_id = request.POST.get('delete_id')
    try:
        CheckpointYearGroup.objects.get(id=cpyg_id).delete()
    except Checkpoint.DoesNotExist:
        return JsonResponse({}, status=404)
    else:
        return JsonResponse({}) 

@login_required
def targets_table(request, cpyg_id: int):
    scope = CheckpointYearGroup.objects.get(id=cpyg_id).checkpoint.scope
    context = {
        'cpyg_id': cpyg_id, 
        'url_data': reverse('checkpoint-yeargroup-targets-data', args=[cpyg_id])
    }
    # Assign URLs and persist is_active in memory
    templates = {
        CheckpointScope.CLASS_LANDMARK: 'checkpoint_class_enrollments_table.html',
        CheckpointScope.SUBJECT_BENCHMARK: 'checkpoint_enrollment_qualifications_table.html',
        CheckpointScope.GENERAL_BENCHMARK: 'checkpoint_enrollments_table.html',
    }
    template = templates.get(scope, None) 
    return render(request, f'register_app/checkpoints/partials/{template}', context)


    
@login_required
def targets_data(request, cpyg_id):
    scope = CheckpointYearGroup.objects.get(id=cpyg_id).checkpoint.scope
    # Store function references 
    response = {
        CheckpointScope.CLASS_LANDMARK: class_enrollments_data,
        CheckpointScope.SUBJECT_BENCHMARK: enrollment_qualifications_data,
        CheckpointScope.GENERAL_BENCHMARK: enrollments_data,
    }
    return response[scope](cpyg_id) 

    
    
def class_enrollments_data(cpyg_id):
    cpyg = (
        CheckpointYearGroup.objects.filter(id=cpyg_id)
        .values("checkpoint_id", "yeargroup_id", "checkpoint__period_id",)
        .first()
    )
    period_id = cpyg["checkpoint__period_id"]
    yeargroup_id = cpyg["yeargroup_id"]

    class_enrollments = ClassEnrollment.objects.select_related(
        "teaching_class__yeargroup",
        "teaching_class__qualification"
    ).filter(
        teaching_class__yeargroup_id=yeargroup_id,
        teaching_class__period_id=period_id 
    )
    data = [
        {
            "id": ce.id,
            "student": str(ce),
            "teaching_class": str(ce.teaching_class),
            "teaching_class_id": ce.teaching_class.id,
            "teachers": ce.teaching_class.get_teachers_display(),
            "qualification": str(ce.teaching_class.qualification),
            "is_active": ce.on_checkpoint(cpyg["checkpoint_id"]),  
            "url_update": reverse(
                'checkpoint-yeargroup-targets-update', 
                kwargs={'cpyg_id': cpyg_id}
            ),
        }
        for ce in class_enrollments
    ]
    return JsonResponse({"data": data})


def enrollment_qualifications_data(cpyg_id):
    cpyg = (
        CheckpointYearGroup.objects.filter(id=cpyg_id)
        .values("checkpoint_id", "yeargroup_id", "checkpoint__period_id")
        .first()
    )
    period_id = cpyg["checkpoint__period_id"]
    yeargroup_id = cpyg["yeargroup_id"]


    enrollment_qualifications = EnrollmentQualification.objects.select_related(
        "enrollment__student", 
        "student_qualification__qualification"
    ).filter(
        enrollment__yeargroup_id=yeargroup_id,
        enrollment__period_id=period_id 
    )
    data = [
        {
            "id": eq.id,
            "student": str(eq.enrollment.student),
            "qualification": str(eq.student_qualification.qualification),
            "qualification_id": eq.student_qualification.qualification.id,
            "is_active": eq.on_checkpoint(cpyg["checkpoint_id"]),  
            "url_update": reverse(
                'checkpoint-yeargroup-targets-update', 
                kwargs={'cpyg_id': cpyg_id}
            ),
        }
        for eq in enrollment_qualifications
    ]
    return JsonResponse({"data": data})


def enrollments_data(cpyg_id):
    cpyg = (
        CheckpointYearGroup.objects.filter(id=cpyg_id)
        .values("checkpoint_id", "yeargroup_id", "checkpoint__period_id")
        .first()
    )
    period_id = cpyg["checkpoint__period_id"]
    yeargroup_id = cpyg["yeargroup_id"]


    enrollments = Enrollment.objects.select_related(
        "student", 
    ).filter(
        yeargroup_id=yeargroup_id,
        period_id=period_id 
    )
    data = [
        {
            "id": enr.id,
            "student": str(enr.student),
            "tags": enr.tags_as_list(),
            "programme": ", ".join(enr.programmes_as_list()),
            "is_active": enr.on_checkpoint(cpyg["checkpoint_id"]),  
            "url_update": reverse(
                'checkpoint-yeargroup-targets-update', 
                kwargs={'cpyg_id': cpyg_id}
            ),
        }
        for enr in enrollments
    ]
    return JsonResponse({"data": data})


@require_POST
@login_required
def update_targets(request, cpyg_id):
    scope = CheckpointYearGroup.objects.get(id=cpyg_id).checkpoint.scope
    data = json.loads(request.body)
    target_ids = [data.get('target_id')]
    grouped_target_id = data.get('grouped_target_id')
    if grouped_target_id and scope == CheckpointScope.CLASS_LANDMARK:
        target_ids=(ClassEnrollment.objects
                .filter(teaching_class_id=grouped_target_id)
                .values_list('id', flat=True)
        )
    elif grouped_target_id and scope == CheckpointScope.SUBJECT_BENCHMARK:
        target_ids=(EnrollmentQualification.objects
                .filter(student_qualification__qualification_id=grouped_target_id)
                .values_list('id', flat=True)
        )
    assign = data.get('status')
    if assign:
        assign_checkpoints(cpyg_id=cpyg_id, target_ids=target_ids)
    else:
        unassign_checkpoints(cpyg_id=cpyg_id, target_ids=target_ids)
    return JsonResponse({})


def assign_checkpoints(cpyg_id, target_ids: list, checkpoint_field_id=None) -> None:
    checkpoint_yeargroup = (
        CheckpointYearGroup.objects
        .select_related("checkpoint")
        .prefetch_related("checkpoint__checkpoint_fields")
        .get(id=cpyg_id)
    )
    scope = checkpoint_yeargroup.checkpoint.scope
    if checkpoint_field_id:
        checkpoint_fields = [CheckpointField.objects.get(id=checkpoint_field_id)]
        print(checkpoint_fields)
    else:
        checkpoint_fields = checkpoint_yeargroup.checkpoint.checkpoint_fields.all()

    if scope==CheckpointScope.CLASS_LANDMARK:
        class_enrollments = ClassEnrollment.objects.filter(id__in=target_ids)
        print(class_enrollments)
        for class_enrollment in class_enrollments:
            class_enrollment.checkpoint_yeargroups.add(cpyg_id)
            
                    # Check if the checkpoint_yeargroup was added
            if class_enrollment.checkpoint_yeargroups.filter(id=cpyg_id).exists():
                print(f"Successfully added checkpoint_yeargroup {cpyg_id} to class_enrollment {class_enrollment.id}")
            else:
                print(f"Failed to add checkpoint_yeargroup {cpyg_id} to class_enrollment {class_enrollment.id}")
        
        
            for checkpoint_field in checkpoint_fields:
                entry, created =CheckpointEntry.objects.get_or_create(
                    checkpoint_yeargroup_id=cpyg_id, 
                    class_enrollment_id=class_enrollment.id,
                    checkpoint_field=checkpoint_field,
                    defaults={
                        "enrollment": class_enrollment.enrollment_qualification.enrollment,
                    }
                )
                if created:
                    print(f"Created CheckpointEntry for checkpoint_field {checkpoint_field.id}")

    elif scope==CheckpointScope.SUBJECT_BENCHMARK:
        enrollment_qualifications = EnrollmentQualification.objects.filter(id__in=target_ids)
        for enrollment_qualification in enrollment_qualifications:
            enrollment_qualification.checkpoint_yeargroups.add(cpyg_id)
            for checkpoint_field in checkpoint_fields:
                CheckpointEntry.objects.get_or_create(
                    checkpoint_yeargroup_id=cpyg_id, 
                    enrollment_qualification_id=enrollment_qualification.id,
                    checkpoint_field=checkpoint_field,
                    defaults={
                        "enrollment": enrollment_qualification.enrollment,
                    }
                )
                
    elif scope==CheckpointScope.GENERAL_BENCHMARK:
        enrollments = Enrollment.objects.filter(id__in=target_ids)
        for enrollment in enrollments:
            enrollment.checkpoint_yeargroups.add(cpyg_id)
            for checkpoint_field in checkpoint_fields:
                CheckpointEntry.objects.get_or_create(
                    checkpoint_yeargroup_id=cpyg_id, 
                    enrollment_id=enrollment.id,
                    checkpoint_field=checkpoint_field,
                    defaults={
                        "checkpoint_field": checkpoint_field,
                    }
                )

def unassign_checkpoints(cpyg_id, target_ids: list)->None:
    checkpoint_yeargroup = (
        CheckpointYearGroup.objects
        .select_related("checkpoint")
        .get(id=cpyg_id)
    )
    scope = checkpoint_yeargroup.checkpoint.scope
    if scope==CheckpointScope.CLASS_LANDMARK:
        class_enrollments = ClassEnrollment.objects.filter(id__in=target_ids).all()
        CheckpointEntry.objects.filter(
                checkpoint_yeargroup_id=cpyg_id, 
                class_enrollment_id__in=target_ids
            ).delete()
        for class_enrollment in class_enrollments:
            class_enrollment.checkpoint_yeargroups.remove(cpyg_id)
    elif scope==CheckpointScope.SUBJECT_BENCHMARK:
        enrollment_qualifications = EnrollmentQualification.objects.filter(id__in=target_ids).all()
        for enrollment_qualification in enrollment_qualifications:
            enrollment_qualification.checkpoint_yeargroups.remove(cpyg_id)
        CheckpointEntry.objects.filter(
                checkpoint_yeargroup_id=cpyg_id, 
                enrollment_qualification_id__in=target_ids
            ).delete()
    elif scope==CheckpointScope.GENERAL_BENCHMARK:
        enrollments = Enrollment.objects.filter(id__in=target_ids).all()
        for enrollment in enrollments:
            enrollment.checkpoint_yeargroups.remove(cpyg_id)
        CheckpointEntry.objects.filter(
                checkpoint_yeargroup_id=cpyg_id, 
                enrollment_id__in=target_ids
            ).delete()
