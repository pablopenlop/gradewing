$(document).ready(function() {
    function scanDocument() {
        // Loop through each form on the page
        $('form').each(function() {
            var $form = $(this);
            var allValid = true;


            if ($form.hasClass('no-validation')) {
                return;
            }

            $form.find('input, select').each(function() {
                
                let $element = $(this);
                let type = $element.attr('type');
                let required = $element.prop('required') || $element.hasClass('required');

                let noblank = $element.hasClass("noblank");
                

                if ((noblank || required) && ['text', 'email', 'date', 'number'].includes(type)) {
                    if ($element.val().trim() === '') {
                        allValid = false;
                        return false; 
                    }
                } else if ($element.is('select') && (noblank || required)) {
                    //console.log('Value:', $element.val());
                    //console.log('ID:', $element.attr('id'));
                    let value= $element.val();
                    if (value === '' || value.length === 0) {
                        allValid = false;
                        return false; 
                    }
                }
            });

            // Modify the submit button state based on validation results
            $form.find('button[type="submit"], input[type="submit"]').prop('disabled', !allValid);
            $form.find('button[type="submit"], input[type="submit"]').removeClass('disabled');
            
        });
    }

    // Initial scan
    scanDocument();

    // Rescan when the DOM is dynamically updated or input changes
    $(document).on('input change', 'input, select', function() {
        scanDocument();
    });

    // Rescan when any button is clicked
    $(document).on('click', 'button, a', function() {
        // Defer scanDocument to run after other logic
        setTimeout(function() {
            scanDocument();
        }, 0);
    });
});


function showAlert(form, errorMessage) {
    // Update the alert message
    form.find('.alert').find('span').text(errorMessage);
    // Show the alert
    form.find('.alert').show();
    // Disable the submit button
    var submitButton = form.find('button[type="submit"]');
    submitButton.prop('disabled', true);
}
