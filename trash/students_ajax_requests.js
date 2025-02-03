$(document).ready(function() {
    $('#add-qualification-form').on('submit', function(event) {
        event.preventDefault(); 
        
        var form = $(this);
        var formData = form.serialize();
        var studentActionValue = $('button[name="students-action"]').val(); 
        formData += '&students_id=' + encodeURIComponent(studentActionValue);
        
        $.ajax({
            url: form.attr('action'), 
            type: 'POST',
            data: formData,
            success: function(response) {
                $('.messages').html(response.messages_html);
                var studentId = $('#details-container').data('student_id')
                var $targetTd = $('#row-details-' + studentId);
                console.log(studentId)
                $targetTd.trigger('click');
            },
            error: function(xhr, status, error) {
                console.log('Error:', error);
            }
        });
    });
});