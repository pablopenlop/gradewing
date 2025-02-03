$(document).ready(function() {
    delayLoading('#school-card-container');

    $(document).on('submit', '#save-school-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                $('#school-form-modal').modal('hide');
                htmx.trigger('#school-card-container', 'refresh');
            },
            error: function(xhr, status, error) {
                $('#school-form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });
});

