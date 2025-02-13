$(document).ready(function() {
    const urlData = window.myAppConfig.urlData;
    const scope = window.myAppConfig.scope; 

    let table; // Global variable to store DataTable instance
    let selectedCell = null; // Store the selected cell for updates

    // Define different configurations
    const tableConfigs = {
        "class_landmark": {
            tableId: "#checkpoint_space-table",
            staticColumns: [
                { data: 'student', title: 'Student' },
                { data: 'teaching_class', title: 'Teaching class' },
                { data: 'class_yeargroup', title: 'Year group' },
                { data: 'teachers', title: 'Teacher' },
                { data: 'qualification', title: 'Qualification' }
            ],
            rowGroupSrc: 'teaching_class',
            rowGroupRender: function(rows, group, staticColumnsLength, dynamicColumnsLength) {
                let teachers = rows.data()[0].teachers;
                let qualification = rows.data()[0].qualification;
                return $('<tr/>').append(`
                    <th colspan="${staticColumnsLength}" style="position: sticky; left: 0px; background-color: rgb(230,230,230);"
                        class="dtfc-fixed-start dtfc-fixed-left">
                        <div class="d-flex align-items-center">
                            <i class="fa-solid fa-chalkboard mx-2 fs-6"></i> ${group}
                            <i class="fa-solid fa-chalkboard-user ms-3 me-2 fs-6"></i> ${teachers}
                            <i class="fa-solid fa-award ms-3 me-2 fs-6"></i> ${qualification}
                        </div>
                    </th>
                    <th colspan="${dynamicColumnsLength}" style="background-color: rgb(230,230,230);"></th>
                `);
            }
        },
        "subject_benchmark": {
            tableId: "#checkpoint_space-table",
            staticColumns: [
                { data: 'student', title: 'Student' },
                { data: 'yeargroup', title: 'Year group' },
                { data: 'qualification', title: 'Qualification' }
            ],
            rowGroupSrc: 'qualification',
            rowGroupRender: function(rows, group, staticColumnsLength, dynamicColumnsLength) {
                return $('<tr/>').append(`
                    <th colspan="${staticColumnsLength}" style="position: sticky; left: 0px; background-color: rgb(230,230,230);"
                        class="dtfc-fixed-start dtfc-fixed-left">
                        <div class="d-flex align-items-center">
                            <i class="fa-solid fa-award mx-2 fs-6"></i> ${group}
                        </div>
                    </th>
                    <th colspan="${dynamicColumnsLength}" style="background-color: rgb(230,230,230);"></th>
                `);
            }
        },
        "general_benchmark": {
            tableId: "#checkpoint_space-table",
            staticColumns: [
                { data: 'student', title: 'Student' },
                { data: 'yeargroup', title: 'Year group' },
                {
                    data: 'tags',
                    title: 'Tags',
                    render: function (data) {
                        return data.map(tag => `<span class="badge rounded-pill badge-dark-secondary my-1 mx-1">
                        ${tag}
                        </span>`).join('');
                    }
                },
                { data: 'programme', title: 'Programme' },
            ],
            rowGroupSrc: 'yeargroup',
            rowGroupRender: function(rows, group, staticColumnsLength, dynamicColumnsLength) {
                return $('<tr/>').append(`
                    <th colspan="${staticColumnsLength}" style="position: sticky; left: 0px; background-color: rgb(230,230,230);"
                        class="dtfc-fixed-start dtfc-fixed-left">
                        <div class="d-flex align-items-center">
                            <i class="fa-solid fa-people-roof mx-2 fs-6"></i> ${group}
                        </div>
                    </th>
                    <th colspan="${dynamicColumnsLength}" style="background-color: rgb(230,230,230);"></th>
                `);
            }
        }
    };

    // Select the correct configuration based on scope
    const config = tableConfigs[scope] || tableConfigs["default"];

    // Fetch data and initialize the table
    $.getJSON(urlData, function(response) {
        const data = response.data || [];
        const dynamicColumns = determineDynamicColumns(data, config.staticColumns);
        table = initDataTable(config, data, dynamicColumns);
        attachEventHandlers(table); 
    });

    function determineDynamicColumns(data, staticColumns) {
        let staticKeys = staticColumns.map(col => col.data);
        let dynamicKeys = [];
        if (data.length > 0) {
            const firstRow = data[0];
            for (const key in firstRow) {
                if (!staticKeys.includes(key)) {
                    dynamicKeys.push(key);
                }
            }
        }
        return dynamicKeys.map(key => ({
            data: key,
            title: key,
            className: "text-center",
            render: function(data) {
                if (data.is_excluded) {
                    return '<i class="fa-solid fa-ban"></i>';
                } else if (!data || data.value === null) {
                    return '<i class="fa-solid fa-pen-to-square"></i>';
                } else {
                    return data.value;
                }
            },
            createdCell: function(td, cellData) {
                $(td).css("min-width", "75px");
                $(td).attr({
                    "data-bs-toggle": "modal",
                    "data-bs-target": "#form-modal-small",
                    "hx-get": cellData.url_form,
                    "hx-target": "#form-container-small"
                });
                htmx.process(td);
            }
        }));
    }

    function initDataTable(config, fetchedData, dynamicColumns) {
        return $(config.tableId).DataTable({
            data: fetchedData,
            columns: config.staticColumns.concat(dynamicColumns),
            columnDefs: [{
                targets: [1],
                orderData: [1, 2, 0]
            },],
            fixedColumns: { start: config.staticColumns.length },
            select: { style: 'single', items: 'cell', toggleable: false },
            scrollX: true,
            deferRender: true,
            stateSave: false,
            order: [[0, 'asc']],
            rowGroup: {
                dataSrc: config.rowGroupSrc,
                startRender: function(rows, group) {
                    return config.rowGroupRender(rows, group, config.staticColumns.length, dynamicColumns.length);
                }
            }
            

        });
    }

    // Attach DataTable events (e.g., cell selection)
    function attachEventHandlers(tableInstance) {
        tableInstance.on('select', function(e, dt, type, indexes) {
            if (type === 'cell') {
                selectedCell = tableInstance.cell(indexes);
            }
        });
    }

    // Handle form submission and update the selected cell upon successful AJAX response
    let action = null;
    $(document).on('click', '#clear-entry-btn', function() {
        action = "clear-entry";
        $('#checkpoint-entry-form').submit();
    });
    $(document).on('click', '#exclude-entry-btn', function() {
        action = "exclude-entry";
        $('#checkpoint-entry-form').submit();
    });


    $(document).on('submit', '#checkpoint-entry-form', function(event) {
        event.preventDefault();
        let form = $(this);
        if (action) {
            $('<input>').attr({
                type: 'hidden',
                name: 'action',
                value: action
            }).appendTo(form);
            action = null;
        }
        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: form.serialize(),
            success: function(response) {
                if (response.success && selectedCell) {
                    let cellData = selectedCell.data();
                    cellData.value = (response.value === null || response.value === undefined) ? null : response.value;
                    cellData.is_excluded = (response.is_excluded === null || response.is_excluded === undefined) ? true : response.is_excluded;
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
