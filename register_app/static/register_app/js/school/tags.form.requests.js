$(document).ready(function() {

    delayLoading('#tags-card-container');
    $(document).on('submit', '#add-tags-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                $('#tags-form-modal').modal('hide');
                htmx.trigger('#tags-card-container', 'refresh');
                
            },
            error: function(xhr, status, error) {
                $('#tags-form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#save-tag-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                if (response.success) {
                    htmx.trigger('#tags-card-container', 'refresh');
                } else {
                    showAlert(form, response.error_message)
                }
            },
            error: function(xhr, status, error) {
                htmx.trigger('#tags-card-container', 'refresh');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#delete-tag-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                htmx.trigger('#tags-card-container', 'refresh');
            },
            error: function(xhr, status, error) {
                htmx.trigger('#tags-card-container', 'refresh');
                $('#error-modal').modal('show');
            }
        });
    });
    
});

