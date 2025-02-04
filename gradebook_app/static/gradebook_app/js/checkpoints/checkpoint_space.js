$(document).ready(function() {
    // Use the global configuration variable
    const urlData = window.myAppConfig.urlData;

    // Define static columns and keys
    const staticColumns = [
        { data: 'student', title: 'Student' },
        { data: 'teaching_class', title: 'Teaching class' },
        { data: 'class_yeargroup', title: 'Year group' },
        { data: 'teachers', title: 'Teacher' },
        { data: 'qualification', title: 'Qualification' }
    ];
    const staticKeys = ['id', 'student', 'teaching_class', 'class_yeargroup', 'teaching_class_id', 'teachers', 'qualification'];

    // Global variables for dynamic columns, DataTable instance, and selected cell
    let dynamicColumns = [];
    let table;
    let selectedCell = null;

    // Fetch JSON data to determine dynamic columns, then initialize DataTable
    $.getJSON(urlData, function(response) {
        const data = response.data || [];
        dynamicColumns = determineDynamicColumns(data, staticKeys);
        initDataTable();
    });

    // Function to compute dynamic columns based on the first row of data
    function determineDynamicColumns(data, staticKeys) {
        let dynamicKeys = [];
        if (data.length > 0) {
            const firstRow = data[0];
            for (const key in firstRow) {
                if (firstRow.hasOwnProperty(key) && staticKeys.indexOf(key) === -1) {
                    dynamicKeys.push(key);
                }
            }
        }
        return dynamicKeys.map(function(key) {
            return {
                data: key,
                title: key,
                className: "text-center",
                render: function(data) {
                    return (!data || data.value === null)
                        ? '<i class="fa-solid fa-pen-to-square"></i>'
                        : data.value;
                },
                createdCell: function(td, cellData) {
                    $(td).attr({
                        "data-bs-toggle": "modal",
                        "data-bs-target": "#form-modal-small",
                        "hx-get": cellData.url_form,
                        "hx-target": "#form-container-small"
                    });
                    htmx.process(td);
                }
            };
        });
    }

    // Initialize the DataTable with the combined (static + dynamic) columns
    function initDataTable() {
        table = $('#checkpoint_space-table').DataTable({
            ajax: { url: urlData, dataSrc: 'data' },
            columns: staticColumns.concat(dynamicColumns),
            columnDefs: [{ orderable: false, targets: [] }],
            fixedColumns: { start: 5 },
            select: { style: 'single', items: 'cell', toggleable: false },
            scrollX: true,
            deferRender: true,
            stateSave: false,
            rowId: 'id',
            order: [[1, 'asc']],
            rowGroup: {
                dataSrc: 'teaching_class',
                startRender: function(rows, group) {
                    let teachers = rows.data()[0].teachers;
                    let qualification = rows.data()[0].qualification;
                    return $('<tr/>').append(`
                        <th colspan="${staticColumns.length}" style="position: sticky; left: 0px; background-color: rgb(230,230,230);"
                            class="dtfc-fixed-start dtfc-fixed-left">
                            <div class="d-flex">
                                <i class="fa-solid fa-chalkboard mx-1"></i> ${group}
                                <i class="fa-solid fa-chalkboard-user ms-3 me-1"></i> ${teachers}
                            </div>
                            <div>
                                <i class="fa-solid fa-award mx-1"></i> ${qualification}
                            </div>
                        </th>
                        <th colspan="${dynamicColumns.length}" style="background-color: rgb(230,230,230);"></th>
                    `);
                }
            }
        });
        attachEventHandlers();
    }

    // Attach DataTable events (e.g., cell selection)
    function attachEventHandlers() {
        table.on('select', function(e, dt, type, indexes) {
            if (type === 'cell') {
                selectedCell = table.cell(indexes);
            }
        });
    }

    // Handle form submission and update the selected cell upon successful AJAX response
    $(document).on('submit', '#checkpoint-entry-form', function(event) {
        event.preventDefault();
        let form = $(this);
        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: form.serialize(),
            success: function(response) {
                if (response.success && selectedCell) {
                    var cellData = selectedCell.data();
                    cellData.value = (response.data === null || response.data === undefined) ? null : response.data;
                    selectedCell.data(cellData).invalidate();
                    table.columns.adjust();
                    $('#form-modal-small').modal('hide');
                }
            },
            error: function() {
                $('#form-modal-small').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });
});
