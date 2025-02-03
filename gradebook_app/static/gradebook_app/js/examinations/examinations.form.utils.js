// Initialize Year Picker
function initializeYearPicker(yearId) {
    var existingValue = $(yearId).val();
    $(yearId).yearpicker();
    $(yearId).val(existingValue);
}


// Enforce Min and Max Limits
function enforceLimits(elementId, minValue, maxValue) {
    $(elementId).on('blur', function() {
        let value = parseFloat($(this).val());
        if (value < minValue) {
            $(this).val(minValue);
        } else if (value > maxValue) {
            $(this).val(maxValue);
        }
    });
}


// REFRESH DATATABLE AND INFOCARD 
function refreshTableAndInfocard(tableId) {
    let table = $(tableId).DataTable();
    let selectedRow = table.row({ selected: true }).node();
    table.ajax.reload(null, false);
     if (selectedRow) {
        selectedRow.click();
    }  
}
