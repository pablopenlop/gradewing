$(document).ready(function() {

    var selectedItems = new Map();
    var count=0;

    let table = new DataTable('#table-element', {
        keys: {
            columns: [1],
            blurable: false
        },
        columnDefs: [
            { orderable: false, "targets": [-1] }, 
            {
                render: DataTable.render.select(),
                targets: 0
            }
        ],
        order: [[2, 'asc']],
        select: {
            style: 'multi',
            selector: 'td:first-child',
        }
    });

    initialiseKeyTable();
    updateView(selectedItems);
    setRequiredSelect('#id_subject');

    table
    .on('key-focus', function (e, datatable, cell) {
        let td = cell.node()
        let studentId = $(td).data('student_id');
        $('#details-container').data('student_id', studentId);
    })
    .on('select', function (e, dt, type, indexes) {
        updateSelectedItems('select', indexes, type);
    })
    .on('deselect', function (e, dt, type, indexes) {
        updateSelectedItems('deselect', indexes, type);
    });
    

    $('#cancel-selection').on('click', function () {
        table.rows().deselect();
    });


    table.rows('.important').deselect();


    function updateSelectedItems(action, indexes, type) {
        indexes.forEach(function(index) { 
            let row = table.row(index).node();  
            let studentId = $(row).data('student_id');
            let studentPeriodId = $(row).data('studentperiod_id');

            if (action === 'select') {
                selectedItems.set(studentId, { studentPeriodId: studentPeriodId });
            } else if (action === 'deselect') {
                selectedItems.delete(studentId);
            }
        });
        updateRowOptions(selectedItems.size>0)
        updateView(selectedItems);
    }

    function updateRowOptions(selected){
        if (selected){
            $('[name="row-options"]').css('visibility', 'hidden');
            return;
        }
        $('[name="row-options"]').css('visibility', 'visible');
    }

    function initialiseKeyTable(){
        var $firstRowDetails = $('[name^="row-details"]').first();
        if ($firstRowDetails.length > 0) {
            htmx.trigger($firstRowDetails[0], 'click');
            studentId = $firstRowDetails.data('student_id');
            $('#details-container').data('student_id', studentId);
        } 
    }

    
});


