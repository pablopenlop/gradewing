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

    # Prefetch only TeachingClasses linked to YearGroups from this Checkpoint
    teaching_classes_qs = (
        TeachingClass.objects
        .filter(period_id=checkpoint.period_id)
        .only('id', 'name', 'period_id')
    )

    # Fetch checkpoint with optimized prefetching
    checkpoint = (
        Checkpoint.objects
        .filter(id=checkpoint_id)
        .prefetch_related(
            Prefetch('checkpoint_yeargroups', queryset=checkpoint_yeargroups_qs),
            Prefetch('checkpoint_yeargroups__yeargroup__teaching_classes', queryset=teaching_classes_qs)
        )
        .only('id', 'period_id')
        .get()
    )

    checkpoint.url_form = reverse('checkpoint-yeargroup-form', args=[checkpoint_id])

    # Assign URLs and persist is_active in memory
    for checkpoint_yeargroup in checkpoint.checkpoint_yeargroups.all():
        checkpoint_yeargroup.url_deleteform = reverse(
            'checkpoint-yeargroup-delete-form',
            args=[checkpoint_yeargroup.id]
        )
        for teaching_class in checkpoint_yeargroup.yeargroup.teaching_classes.all():
            teaching_class.is_active = teaching_class.is_active_in_checkpoint(checkpoint.id)

    context = {'checkpoint': checkpoint}
    return render(request, 'register_app/checkpoints/partials/checkpoint_targets_card.html', context)
