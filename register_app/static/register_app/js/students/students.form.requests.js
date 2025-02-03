$(document).ready(function() {

    delayLoading('#students-table-card');
    delayLoading('#student-infocard-container');
    
    $(document).on('submit', '#student-delete-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                htmx.trigger('#students-headerbar', 'refresh');
                delayLoading('#students-table-card');
                $('#delete-modal').modal('hide');
            },
            error: function(xhr, status, error) {
                $('#delete-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#student-general-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                if (response.success) {
                    $('#form-modal').modal('hide');
                    window.location.href = response.redirect_url;
                } else {
                    showAlert(form, response.error_message)
                }
            },
            error: function(xhr, status, error) {
                $('#form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });


});

