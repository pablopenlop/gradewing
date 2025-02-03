$(document).ready(function() {
    delayLoading('#details-card-container');
    delayLoading('#fields-card-container');
    delayLoading('#targets-card-container');
    
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
                    htmx.trigger('#details-card-container', 'refresh');
                    delayLoading('#details-card-container');
                    $('#form-modal').modal('hide');
                } else {
                    form.find('.alert').find('span').text(response.error_message);
                    form.find('.alert').show();
                    var submitButton = form.find('button[type="submit"]');
                    submitButton.prop('disabled', true);
                }
            },
            error: function(xhr, status, error) {
                $('#form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#checkpointfield-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                if (response.success) {
                    htmx.trigger('#fields-card-container', 'refresh');
                    delayLoading('#fields-card-container');
                    $('#form-modal').modal('hide');
                } else {
                    form.find('.alert').find('span').text(response.error_message);
                    form.find('.alert').show();
                    var submitButton = form.find('button[type="submit"]');
                    submitButton.prop('disabled', true);
                }
            },
            error: function(xhr, status, error) {
                $('#form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#checkpoint-yeargroup-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                delayLoading('#targets-card-container');
                delayLoading('#fields-card-container');
                delayLoading('#details-card-container');
                htmx.trigger('#targets-card-container', 'refresh');
                $('#form-modal').modal('hide');
            },
            error: function(xhr, status, error) {
                $('#form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });



    $(document).on('submit', '#delete-checkpointfield-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                delayLoading('#fields-card-container');
                htmx.trigger('#fields-card-container', 'refresh');
                $('#field-delete-modal').modal('hide');
            },
            error: function(xhr, status, error) {
                $('#field-delete-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#checkpoint-yeargroup-delete-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                delayLoading('#fields-card-container');
                delayLoading('#details-card-container');
                delayLoading('#targets-card-container');
                htmx.trigger('#targets-card-container', 'refresh');
                $('#delete-modal').modal('hide');
            },
            error: function(xhr, status, error) {
                $('#delete-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    // function delayLoading(divId) {
    //     $(divId).css('visibility', 'hidden'); // Hide initially
    //     setTimeout(function() {
    //         $(divId).css('visibility', '').hide().fadeIn(300); // Reset visibility and apply fade-in
    //     }, 200);
    // }

});

