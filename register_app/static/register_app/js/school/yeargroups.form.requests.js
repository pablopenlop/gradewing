$(document).ready(function() {
    delayLoading('#yeargroups-card-container');
    $(document).on('submit', '#custom-yeargroup-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                if (response.success) {
                    $('#custom-yeargroup-form-modal').modal('hide');
                    htmx.trigger('#yeargroups-card-container', 'refresh');
                } else {
                    showAlert(form, response.error_message)
                    /* form.find('#custom-yeargroup-form-error-alert').find('span').text(response.error_message);
                    form.find('#custom-yeargroup-form-error-alert').show();
                    var submitButton = $('#custom-yeargroup-form').find('button[type="submit"]');
                    submitButton.prop('disabled', true); */
                }
            },
            error: function(xhr, status, error) {
                $('#custom-yeargroup-form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });
});

