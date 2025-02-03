$(document).ready(function() {

    $(document).on('click', '.dropdown-item[name="period-delete"]', function() {
        const periodId = $(this).data('period_id');
        $('#confirmDelete').val(periodId);

    });

    $('#add-period-modal').on('hide.bs.modal', function () {
        $('#add-period-trigger').one('focus', function () {
            $(this).blur();
        });
    });


    $(document).on('click', '[name="period-card"]', function() {
        const periodId = $(this).data('period_id');
        console.log("trig")
        $('[name="period-card"]').removeClass('active');
        $('#period-card-' + periodId).addClass('active');
        $('[name="period-card-chevron"]').css('visibility', 'hidden');
        $('#period-card-chevron-' + periodId).css('visibility', 'visible');

    });

    
});
