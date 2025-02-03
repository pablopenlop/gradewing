(function ($) {
    $.fn.maxlength = function () {
        this.each(function () {
            let maxlength = $(this).attr('maxlength');
            let length = $(this).val().length;

            // Add counter dynamically without replacing the original structure
            if (!$(this).next('.maxlength-counter').length) {
                let counter = $('<div></div>')
                    .addClass('d-flex justify-content-end small maxlength-counter')
                    .css('margin-top', '0.25rem')
                    .css('margin-right', '1rem')
                    .append($('<span></span>').addClass('length').html(length))
                    .append('/')
                    .append(maxlength);

                $(this).after(counter);
            }
        });
    };
})(jQuery);

$(() => {
    $(document).on('keyup', '[maxlength]', function () {
        let length = $(this).val().length;
        $(this).next('.maxlength-counter').find('.length').html(length);
    });

    // Initialize plugin
    $('[maxlength]').maxlength();
});
