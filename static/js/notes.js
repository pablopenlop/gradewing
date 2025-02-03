
// Event delegation: Handles dynamically added elements
$(document).on('change', 'input[name="row-selector"]', handleRowSelectorChange);

// Direct binding: Only handles elements present at the time of binding
$('[name="row-selector"]').on('change', handleRowSelectorChange);


const myMap = new Map([
    ['key1', 'value1'],
    ['key2', 'value2'],
    ['key3', 'value3']
]);

const mySet = new Set(['value1', 'value2', 'value3']);

//displayMapContents(myMap, 'mapp');
//displaySetContents(mySet, 'sett');



function displayMapContents(map, elementId) {
    const mapContents = [];
    map.forEach((value, key) => {
        mapContents.push(`${key}: ${value}`);
    });
    $(`#${elementId}`).html(`Map Contents:<br>${mapContents.join('<br>')}`);
}

// Function to display Set contents
function displaySetContents(set, elementId) {
    const setContents = Array.from(set).join('<br>');
    $(`#${elementId}`).html(`Set Contents:<br>${setContents}`);
}

        //$('[name="row-element"]').click(handleRowClick);
        //$('[name="row-checkbox"]').change(handleRowCheckboxChange);
        //$('#header-checkbox').change(handleHeaderCheckboxChange);
        //$('#cancel-selection').click(handleCancelSelection);
        //$('#table-element').on('page order search draw', handleTableChange);  


        $('[id^="id_periods-"][id$="-programme"]').each(function() {
            $(this).selectize({
                plugins: ["remove_button"],
                delimiter: ",",
                persist: false,
                placeholder: 'Select subject areas ...',
                create: function (input) {
                    return {
                        value: input,
                        text: input,
                    };
                },
            });
        });



    $(document).on('htmx:afterOnLoad', function(event) {
        console.log('HTMX request successfully loaded the response!');
        
    });


    dropdown.tooltip();
    dropdown.attr('data-bs-title', selectedText);
    dropdown.tooltip('dispose').tooltip('show');




    
    $(document).ready(function () {
        // Initialize Selectize
        const select = $('#select-pass-fail').selectize({
            plugins: ["remove_button"],
            options: [
                { value: 'pass_fail', text: 'Pass / Fail' },
                { value: '5tier_general', text: 'Five-tier general descriptors' },
                { value: '4tier_behaviour', text: 'Four-tier behaviour descriptors' },
            ],
            create: true, // Disable creating new tags
            
            onItemAdd: function (value) {
                // Check if the selected item is Pass / Fail
                if (value === 'pass_fail') {
                    const selectize = this;
    
                    // Add "Pass" and "Fail" dynamically
                    selectize.addOption({ value: 'Pass', text: 'Pass' });
                    selectize.addOption({ value: 'Fail', text: 'Fail' });
    
                    // Add both as selected items
                    selectize.addItem('Pass');
                    selectize.addItem('Fail');
    
                    // Remove the Pass / Fail placeholder
                    selectize.removeItem('pass_fail', true);
                }
                else if (value === '5tier_general') {
                    const selectize = this;
                    selectize.addOption({ value: 'Excellent', text: 'Excellent' });
                    selectize.addOption({ value: 'Very good', text: 'Very good' });
                    selectize.addOption({ value: 'Good', text: 'Good' });
                    selectize.addOption({ value: 'Fair', text: 'Fair' });
                    selectize.addOption({ value: 'Poor', text: 'Poor' });
    
                    // Add both as selected items
                    selectize.addItem('Excellent');
                    selectize.addItem('Very good');
                    selectize.addItem('Good');
                    selectize.addItem('Fair');
                    selectize.addItem('Poor');
    
                    // Remove the Pass / Fail placeholder
                    selectize.removeItem('5tier_general', true);
                }
                this.$dropdown.hide();
                this.focus();
            }

        });

    });