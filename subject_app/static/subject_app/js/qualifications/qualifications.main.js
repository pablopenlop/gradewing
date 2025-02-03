$(document).ready(function() {
const divId = '#family-main-content';
    function delayLoading(divId) {
        $(divId).css('visibility', 'hidden');
        setTimeout(function() {
            $(divId).css('visibility', 'visible');
        }, 250);
    }
    
    delayLoading(divId);
    
    $('button[name="family-nav-tabs"]').on('click', function() {
        $('button[name="family-nav-tabs"]').removeClass('active');
        $(this).addClass('active');
        delayLoading(divId);
    });

    

});
