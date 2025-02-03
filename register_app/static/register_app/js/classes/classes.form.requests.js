$(document).ready(function() {
    delayLoading('#classes-table-card');

    $(document).on('submit', '#class-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                if (response.success) {
                    htmx.trigger('#classes-headerbar', 'refresh');
                    delayLoading('#classes-table-card');
                    $('#class-form-modal').modal('hide');

                } else {
                    form.find('.alert').find('span').text(response.error_message);
                    form.find('.alert').show();
                    var submitButton = form.find('button[type="submit"]');
                    submitButton.prop('disabled', true);
                }
            },
            error: function(xhr, status, error) {
                $('#class-form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#delete-class-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                htmx.trigger('#classes-headerbar', 'refresh');
                delayLoading('#classes-table-card');
                $('#class-delete-modal').modal('hide');
            },
            error: function(xhr, status, error) {
                $('#classes-delete-modal').modal('hide');
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

