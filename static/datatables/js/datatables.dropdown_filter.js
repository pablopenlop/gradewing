/* function initializeDropdownFilter(table, columnIndex, selectElementId) {
    // Get the state and set the correct option in the select dropdown upon load
    let state = table.state(); // Get the DataTable state
    if (state && state.columns[columnIndex].search.search) {
        let columnFilter = state.columns[columnIndex].search.search;
        let match = columnFilter.match(/\b(.+?)\b/); // Match the value between \b...\b
        console.log(columnFilter, match)
        if (match) {
            columnFilter = match[1]; // Extract the actual value
        }
        let selectElement = document.getElementById(selectElementId);
        let optionExists = Array.from(selectElement.options).some(option => option.value === columnFilter);

        if (optionExists) {
            selectElement.value = columnFilter; // Set the value if the option exists
        } else {
            selectElement.selectedIndex = 0; // Select the first option
            table.columns(columnIndex).search('').draw();
        }
    }

    // Event listener for the select element
    document.getElementById(selectElementId).addEventListener('change', function (e) {
        let filterValue = e.target.value;
        if (filterValue) {
            let regexFilter = `\\b${filterValue}\\b`; // Match the exact value as a whole word
            table.columns(columnIndex).search(regexFilter, true, false).draw();
        } else {
            table.columns(columnIndex).search('').draw();
        }
    });
}
 */


function initializeDropdownFilter(table, columnIndex, selectElementId) {
    // Ensure DataTable state saving is enabled
    let state = table.state(); // Get the saved DataTable state

    if (state && state.columns[columnIndex].search.search) {
        let columnFilter = state.columns[columnIndex].search.search;

        // Remove the regex if it's saved with \b...\b format
        if (columnFilter.startsWith('\\b') && columnFilter.endsWith('\\b')) {
            columnFilter = columnFilter.slice(2, -2); // Extract the exact value
        }

        console.log('Restoring filter:', columnFilter);

        // Set the dropdown value if the option exists
        let selectElement = document.getElementById(selectElementId);
        let optionExists = Array.from(selectElement.options).some(option => option.value === columnFilter);

        if (optionExists) {
            selectElement.value = columnFilter;
        } else {
            selectElement.selectedIndex = 0; // Default to the first option if the value doesn't exist
        }
    }

    // Event listener for dropdown change
    const selectElement = document.getElementById(selectElementId);
    selectElement.addEventListener('change', function (e) {
        let filterValue = e.target.value;

        if (filterValue) {
            let regexFilter = `\\b${filterValue}\\b`; // Save as exact match
            table.columns(columnIndex).search(regexFilter, true, false).draw();
        } else {
            table.columns(columnIndex).search('').draw();
        }
    });

    // Save column filter to the state whenever it changes
    table.on('stateSaveParams.dt', function (e, settings, data) {
        let currentFilter = selectElement.value;
        if (currentFilter) {
            data.columns[columnIndex].search.search = `\\b${currentFilter}\\b`; // Save filter as exact match
        } else {
            data.columns[columnIndex].search.search = ''; // Clear filter if no value
        }
    });
}
