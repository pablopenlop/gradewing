$(document).ready(function() {
    delayLoading('#periods-card-container');
    $(document).on('submit', '#save-period-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                if (response.success) {
                    $('#period-form-modal').modal('hide');
                    htmx.trigger('#periods-card-container', 'refresh');
                } else {
                    showAlert(form, response.error_message)
                }
            },
            error: function(xhr, status, error) {
                $('#period-form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#period-delete-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                $('#delete-modal').modal('hide');
                $('#reload-periods-card').click();
            },
            error: function(xhr, status, error) {
                $('#delete-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });
});

