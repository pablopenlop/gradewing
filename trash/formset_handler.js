function handleFormset(maxCount, maxCountAllowed, relatedName, formName) {
    console.log(relatedName)
    function getCount() {
        var count = maxCount;
        $('[id^="id_' + relatedName +'-"][id*="-DELETE"]').each(function() {
            if ($(this).is(':checked')) {
                count--;
            }
        });
        return count;
    }

    function adaptFormset(count) {
        $('#' + formName + '-count').text(count);
        for (var i = 1; i <= count; i++) {
            $('#' + formName + '-card-' + i).show();
            $('#delete-' + formName + '-' + i).hide();
            $('#id_' + relatedName +'-' + (i - 1) + '-DELETE').prop('checked', false);
            $('#id_' + relatedName +'-' + (i - 1) + '-subject').prop('required', true);
            $('#id_' + relatedName +'-' + (i - 1) + '-programme').prop('required', true);
            $('#id_' + relatedName +'-' + (i - 1) + '-yeargroup').prop('required', true);
            $('#id_' + relatedName +'-' + (i - 1) + '-subject_areas').addClass('noblank');
            console.log($('#id_' + relatedName +'-' + (i - 1) + '-subject_areas'))
        }
        for (var j = count + 1; j <= maxCount; j++) {
            $('#' + formName + '-card-' + j).hide();
            $('#id_' + relatedName +'-' + (j - 1) + '-DELETE').prop('checked', true);
            $('#id_' + relatedName +'-' + (j - 1) + '-subject').prop('required', false);
            $('#id_' + relatedName +'-' + (j - 1) + '-programme').prop('required', false);
            $('#id_' + relatedName +'-' + (j - 1) + '-yeargroup').prop('required', false);
            $('#id_' + relatedName +'-' + (j - 1) + '-subject_areas').removeClass('noblank');

        }
        if (count > 1) {
            $('#delete-' + formName + '-' + count).show();
        }
        if (count === maxCountAllowed) {
            $('#add-' + formName + '').css('visibility', 'hidden');
        } else {
            $('#add-' + formName + '').css('visibility', 'visible');
        }
    }
    function scrollToElement(count) {
        const $targetElement =  $('#' + formName + '-card-' + (count));
        const offset = $targetElement.offset().top - ($(window).height() / 2) 
        + ($targetElement.outerHeight() / 2);
        $('html, body').animate({ scrollTop: offset }, 100);
    }

    $(document).ready(function() {
        var count = getCount();
        adaptFormset(count);
    });

    $('#add-' + formName + '').on('click', function() {
        var count = getCount();
        adaptFormset(++count);
        scrollToElement(count);
    });

    $('[name="delete-' + formName + '"]').on('click', function() {
        var count = getCount();
        adaptFormset(--count);
    });
}
