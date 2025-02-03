
function handleFormset(maxcount, relatedName) {
    
    function getCount(){
        var count = maxcount;
        var deleteElements = $('[id^="id_' + relatedName +'-"][id*="-DELETE"]');
        deleteElements.each(function() {
            if ($(this).is(':checked')) {
                count--;
                }
            });
        return count;
        }

        function adaptFormset(count) {
            $('#enrollmentCount').text(count);
            for (var i = 1; i <= count; i++) {
                $('#enrollmentCard_' + i).show();
                $('#deleteEnrollment_' + i).hide()
                $('#id_' + relatedName +'-' + (i-1) + '-DELETE').prop('checked', false);
            }
            for (var j = count + 1; j <= maxcount; j++) {
                $('#enrollmentCard_' + j).hide();
                $('#id_' + relatedName +'-' + (j-1) + '-DELETE').prop('checked', true);
            }
            if (count>1) { 
                $('#deleteEnrollment_' + count).show();
                }  
            if (count === maxcount) {
                $('#addEnrollment').hide();
                }
            else {
                $('#addEnrollment').show();
                }
        
        }

    $(document).ready(function() {
        var count = getCount();
        adaptFormset(count);
    });

    $(document).on('click', '#addEnrollment', function() {
        var count = getCount();
        count++;
        adaptFormset(count);

    });

    $(document).on('click', 'button[name="delete-enrollment"]', function() {
        var count = getCount();
        count--;
        adaptFormset(count);

    });
}
