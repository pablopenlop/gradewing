$(document).ready(function() {
    
    $(document).on('submit', '#qualification-exam-result-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                if (response.success) {
                    refreshTableAndInfocard('#examinations-table');
                    $('#qualification-exam-result-form-modal').modal('hide');
                } else {
                    showAlert(form, response.error_message)
                }
            },
            error: function(xhr, status, error) {
                $('#qualification-exam-result-form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });
    $(document).on('submit', '#component-exam-result-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                if (response.success) {
                    refreshTableAndInfocard('#examinations-table');
                    $('#component-exam-result-form-modal').modal('hide');
                } else {
                    showAlert(form, response.error_message)
                }
            },
            error: function(xhr, status, error) {
                $('#component-exam-result-form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#linear-qualification-exam-result-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                
                if (response.success) {
                    console.log("SUCCESS")
                    refreshTableAndInfocard('#examinations-table');
                    $('#linear-qualification-exam-result-form-modal').modal('hide');
                } else {
                    showAlert(form, response.error_message)


                }
            },
            error: function(xhr, status, error) {
                $('#linear-qualification-exam-result-form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#qualification-exam-result-delete', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                    $('#qualification-exam-result-delete-modal').modal('hide');
                if (response.success) {
                    refreshTableAndInfocard('#examinations-table');
                } else {
                    $('#error-modal').modal('show');
                }
            },
            error: function(xhr, status, error) {
                $('#qualification-exam-result-delete-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#component-exam-result-delete', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                    $('#component-exam-result-delete-modal').modal('hide');
                if (response.success) {
                    refreshTableAndInfocard('#examinations-table');
                } else {
                    $('#error-modal').modal('show');
                }
            },
            error: function(xhr, status, error) {
                $('#component-exam-result-delete-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    


});