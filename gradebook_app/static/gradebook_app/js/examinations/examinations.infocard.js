
$(document).ready(function() {

    // TOOLTIPS
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // CARD HEIGHT
    const margin = 160;
    let newHeight = Math.max($(window).height()-margin, 400); 
    $('#info-card').css('max-height', newHeight + 'px');
    
    // COMPONENT EXAM RESULT DROPDOWN 
    if ($('#add-component-exam-result').length) {
        $('#add-component-exam-result').on('show.bs.dropdown', function() {
            var $dropdown = $('#cer-dropdown');
            let width = $('#info-card-body').width();
            var $infoCard = $('#info-card');
            let newHeight = Math.max($(window).height() - margin, 400); 
            $infoCard.css('height', newHeight + 'px');
            $dropdown.css('width', width + 'px');
        });
        $('#add-component-exam-result').on('hide.bs.dropdown', function() {

            var $infoCard = $('#info-card');
            $infoCard.css('height', '');

        });
    }


});
        
        
