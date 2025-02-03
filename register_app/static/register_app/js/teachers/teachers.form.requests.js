$(document).ready(function() {
    delayLoading('#teachers-table-card');

    $(document).on('submit', '#save-teacher-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                if (response.success) {
                    $('#teacher-form-modal').modal('hide');
                    htmx.trigger('#teachers-headerbar', 'refresh');
                    delayLoading('#teachers-table-card');

                } else {
                    form.find('.alert').find('span').text(response.error_message);
                    form.find('.alert').show();
                    var submitButton = form.find('button[type="submit"]');
                    submitButton.prop('disabled', true);
                }
            },
            error: function(xhr, status, error) {
                $('#teacher-form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#delete-teacher-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                delayLoading('#teachers-table-card');
                $('#teacher-delete-modal').modal('hide');
                htmx.trigger('#teachers-headerbar', 'refresh');
                
            },
            error: function(xhr, status, error) {
                $('#teacher-delete-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });



    /*     function delayLoading(divId) {
        $(divId).css('visibility', 'hidden'); // Hide initially
        setTimeout(function() {
            $(divId).css('visibility', '').hide().fadeIn(300); // Reset visibility and apply fade-in
        }, 200);
    } */

});

