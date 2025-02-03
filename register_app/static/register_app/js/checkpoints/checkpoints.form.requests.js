$(document).ready(function() {

    delayLoading('#checkpoints-table-card');
    
    $(document).on('submit', '#checkpoint-delete-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                htmx.trigger('#checkpoints-headerbar', 'refresh');
                delayLoading('#checkpoints-table-card');
                $('#delete-modal').modal('hide');
            },
            error: function(xhr, status, error) {
                $('#delete-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#checkpoint-preform-2', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                if (response.success) {
                    $('#checkpoint-form-modal').modal('hide');
                    window.location.href = response.redirect_url;
                } else {
                    form.find('.alert').find('span').text(response.error_message);
                    form.find('.alert').show();
                    var submitButton = form.find('button[type="submit"]');
                    submitButton.prop('disabled', true);
                }
            },
            error: function(xhr, status, error) {
                $('#checkpoint-form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    function delayLoading(divId) {
        $(divId).css('visibility', 'hidden'); // Hide initially
        setTimeout(function() {
            $(divId).css('visibility', '').hide().fadeIn(300); // Reset visibility and apply fade-in
        }, 200);
    }

});

