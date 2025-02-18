$(document).ready(function() {

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
                    htmx.trigger('#general-card-container', 'refresh');
                    htmx.trigger('#enrollments-card-container', 'refresh');

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

    $(document).on('submit', '#student-enrollment-form', function(event) {
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
                    htmx.trigger('#enrollments-card-container', 'refresh');

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

    $(document).on('submit', '#student-enrollment-delete-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                htmx.trigger('#enrollments-card-container', 'refresh');
                $('#delete-modal').modal('hide');
            },
            error: function(xhr, status, error) {
                $('#delete-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on(
        'submit', 
        '#student-qualification-form, #student-programme-form',
        function(event) {
            event.preventDefault(); 
            var form = $(this)
            var formData = form.serialize(); 
            $.ajax({
                url: form.attr('action'), 
                type: 'POST', 
                data: formData, 
                success: function(response) {
                    if (response.requires_confirmation) {
                        showAlert(form, response.message)
                    } else {
                        $('#form-modal').modal('hide')
                        htmx.trigger('#qualifications-card-container', 'refresh');
                    }
                },
                error: function(xhr, status, error) {
                    $('#form-modal').modal('hide');
                    $('#error-modal').modal('show');
                }
            }
        );
    });


    $(document).on(
        'submit', 
        '#student-qualification-delete-form, #student-programme-delete-form',
        function(event) {
            event.preventDefault(); 
            var form = $(this)
            var formData = form.serialize(); 
            $.ajax({
                url: form.attr('action'), 
                type: 'POST', 
                data: formData, 
                success: function(response) {
                        $('#delete-modal').modal('hide')
                        htmx.trigger('#qualifications-card-container', 'refresh');
                },
                error: function(xhr, status, error) {
                    $('#delete-modal').modal('hide');
                    $('#error-modal').modal('show');
                }
            }
        );
    });




    function delayLoading(divId) {
        $(divId).css('visibility', 'hidden'); // Hide initially
        setTimeout(function() {
            $(divId).css('visibility', '').hide().fadeIn(300); // Reset visibility and apply fade-in
        }, 200);
    }

});

