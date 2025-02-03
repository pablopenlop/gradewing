$(document).ready(function() {
    $(document).on('submit', '#save-period-form', function(event) {
        event.preventDefault(); 

        var form = $(this);
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                console.log(response); 
                
                if (response.success) {
                    console.log('Form submitted successfully.');
                    var periodId = response.periodId;
                    $('#period-modal').modal('hide');
                    $("#active_id").val(periodId);
                    $("#refresh_periods").click();

                } else {
                    console.log('Form submission failed, updating form content.');
                    $('#period-form-container').html(response.html);
                }
            },
            error: function(xhr, status, error) {
                console.log('AJAX request error:', error); // Handle errors here
            }

        });
    });
});