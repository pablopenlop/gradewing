$(document).ready(function() {

    var selectedItems = new Map();
    var selectionMode = true;
    var activeId = 0;

    var table = new DataTable('#table-element', {
        columnDefs: [
            { orderable: false, "targets": [1, -1] }, 
            {
                render: DataTable.render.select(),
                targets: 0
            }
        ],
        order: [[2, 'asc']],
        select: {
            style: 'multi',
            selector: '.dt-select-checkbox',
        }
    });

    /* var table = new DataTable('#table-element', {
        columnDefs: [
            { orderable: false, "targets": [0, -1] }, 
            
        ],
        order: [[2, 'asc']],
    }); 


    var headerCell = $(table.column(1).header());
    console.log(headerCell)



// Insert a new non-clickable span before the clickable content
headerCell.prepend('<div class="mx-3" id ="hello"><input class="form-check-input mx-3" type="checkbox" id="selectAll" name="header-checkbox"></div>');
headerCell.addClass("dt-select")

var updatedHeaderHtml = headerCell.html();
table.column(1).header().innerHTML = updatedHeaderHtml;
table.draw(false)

var headerCell = $(table.column(0).header());
headerCell.addClass("dt-select")
*/










    bindEvents();
    updateBar();
    displaySelection();
    setDefaultDetails();


    function setDefaultDetails(){
        var $firstRowDetails = $('[name^="row-details"]').first();
        htmx.trigger($firstRowDetails[0], 'click');
        activeId = $firstRowDetails.data('student_id');
    }

    function bindEvents() {
        $(document).on('click', '[name="row-details"]', handleRowDetailsClick);
        $(document).on('click', '[name="row-checkbox"]', handleRowCheckboxClick);
        $(document).on('click', '[name^="row-options"]', handleRowOptionsClick);
        $(document).on('click', '[name="row-element"]', handleRowClick);
        $(document).on('click', '[name="header-checkbox"]', handleHeaderCheckboxClick);
        $(document).on('click', '#hello', handleHeaderClick);
        $(document).on('click', '#cancel-selection', handleCancelSelection);
        $(document).on('page.dt order.dt search.dt draw.dt', '#table-element', handleTableChange);
        $(document).on('click', '[name="row-options-delete-student"]', handleStudentDeleteClick);
    }

    function handleHeaderClick(e) {
        var order = table.order();
        table.order(order).draw();

    }
    function handleRowCheckboxClick() {
        $(this).prop('checked', !$(this).prop('checked'));
    }

    function handleRowDetailsClick() {
        activeButton = $(this);
        activeId = $(this).data('student_id');
        setActiveDetailsButton()
        selectionMode = false;
    }

    function handleRowOptionsClick() {
        selectionMode = false;
    }

    function handleRowClick() {
        if (!selectionMode){
            selectionMode = true;
            return;
        }
        var id = $(this).data("student_id");
        var checkbox = $("#row-checkbox-" + id);
        $(this).toggleClass('table-active');
        checkbox.prop('checked', !checkbox.prop('checked'));
        updateItemsByRow(checkbox);
        updateBar();
        displaySelection();
    }

    function setActiveDetailsButton(){
        $('[name="row-details"]').each(function() {
            const value = $(this).data('student_id');
            if (activeId===value) {
                $(this).addClass('active');
            } else {
                $(this).removeClass('active');
            }
        });
    }
  
    function handleCancelSelection() {
        uncheckAll();
        updateBar();
        displaySelection();
          
    }


    function handleHeaderCheckboxClick(e) {
        e.stopPropagation();
        console.log($(this).prop('checked'))
        updateItemsByHeader($(this).prop('checked'));
        updateBar();
        displaySelection();
        
        
        
    }

    function updateItemsByHeader(isChecked) {
        $('input[name="row-checkbox"]').each(function() {
            const studentId = $(this).data('student_id');
            const studentPeriodId = $(this).data('studentperiod_id');
            const studentName = $("#row-details-"+(studentId)).text();
            if (isChecked) {
                addItem(studentId, studentPeriodId, studentName)
                $("#row-element-" + studentId).addClass('table-active');
                setSelectedOrder(studentId, studentName); 
            } else {
                selectedItems.delete(studentId);
                $("#row-element-" + studentId).removeClass('table-active');
                setSelectedOrder(studentId, '\uFFFD'); 

            }
            $(this).prop('checked', isChecked);
        });
        
    }


    function setSelectedOrder(studentId, orderValue) {
        $('#text-select-' + studentId).text(orderValue);
        var cell = table.cell('#row-select-' + studentId);
        var updatedHtml = $('#row-select-' + studentId).html();
        cell.data(updatedHtml).draw(false);
    }

    function updateItemsByRow(element) {
        const studentId = $(element).data('student_id');
        const studentPeriodId = $(element).data('studentperiod_id');
        const studentName = $("#row-details-"+(studentId)).text();
   
        if ($(element).prop('checked')) {
            addItem(studentId, studentPeriodId, studentName)
            setSelectedOrder(studentId, studentName);        
  
        }
            
        else {
                selectedItems.delete(studentId);
                $('[name="header-checkbox"]').prop('checked', false);      
                setSelectedOrder(studentId, '\uFFFD'); 
            }

    }

    function updateBar() {
        const count = selectedItems.size;
        const text = count === 1 ? "student" : "students";
        $('span[name="item-label"]').text(text);
        
        updateStudentActions();
        updateStudentPeriodActions();
        setHeaderCheckbox();

        $('#itemCount').text(count);

        if (count > 0){
            $('#period_id').prop('disabled', true); 
            $('#optionsBar').show();
            $('#utilityBar').hide();
            $('button[name="row-options"]').prop('disabled', true); 
            
        } else {
            $('#period_id').prop('disabled', false); 
            $('#optionsBar').hide();
            $('#utilityBar').show();
            $('button[name="row-options"]').prop('disabled', false); 
            
        }
    }

    function uncheckAll() {
        selectedItems.clear();
        table.rows().every(function() {
            var rowNode = this.node();
            $(rowNode).removeClass('table-active');
            $(rowNode).find('input[name="row-checkbox"]').prop('checked', false);
            var $cell = $(rowNode).find('td[name="row-select"]');
            var $text = $(rowNode).find('span[name="text-select"]');
            $text.text('\uFFFD');
            this.cell($cell).data($cell.html());
        });
        table.draw(false);
        $('[name="header-checkbox"]').prop('checked', false);

    }

    function setSelectedRows(){

        $('[name="header-checkbox"]').prop('checked', false);
        $('input[name="row-checkbox"]').each(function() {
            const rowId = $(this).data('student_id');
            $(this).prop('checked', selectedItems.has(rowId));
        });
        $('[name="row-element"]').each(function() {
            const value = $(this).val();
            if (selectedItems.has(value)) {
                $(this).addClass('active');
            } else {
                $(this).removeClass('active');
            }
        });
    }

    function setHeaderCheckbox(){
        
        const count = selectedItems.size;

        if (count === 0) {
            $('[name="header-checkbox"]').prop('indeterminate', false);
            $('[name="header-checkbox"]').prop('checked', false);
            return;
        }

        $('[name="header-checkbox"]').prop('checked', true);
        $('[name="header-checkbox"]').prop('indeterminate', false);
        
        $('input[name="row-checkbox"]').each(function() {
            if ($(this).prop('checked')===false){
                $('[name="header-checkbox"]').prop('indeterminate', true);
                $('[name="header-checkbox"]').prop('checked', false);
                return;
            }
        }); 
    }

    function handleTableChange() {
        setActiveDetailsButton();
        setSelectedRows();
        setHeaderCheckbox();
    }

    function displaySelection() {
        if (selectedItems.size===0) {
            $('#selection-list-container').hide();
            return;
        }

        var $ul = $('ul[name="selection-list"]');
        $ul.empty();
        
        var sortedItems = Array.from(selectedItems.entries()).sort(function(a, b) {
            return a[1].studentName.localeCompare(b[1].studentName);
        });
    
        // Iterate over the sorted array and create list items
        sortedItems.forEach(function([key, value], index) {
            var $li = $('<li></li>').html(
                '<i class="fa-regular fa-square-check"></i>'
                + '&nbsp;&nbsp;' + (index + 1) + '. &nbsp;&nbsp;' 
             + value.studentName);
            $ul.append($li);
        });
        $('#selection-list-container').show()
    }

    function addItem(studentId, studentPeriodId, studentName) {
        selectedItems.set(studentId, { studentPeriodId: studentPeriodId, studentName: studentName });
    }

    function updateStudentActions() {
        var idList = Array.from(selectedItems.keys());
        var idString = idList.join(',');
        $('[name="students-action"]').val(idString);
    }

    function updateStudentPeriodActions() {
        var periodIdList = Array.from(selectedItems.values()).map(item => item.studentPeriodId);
        var periodIdString = periodIdList.join(',');
        $('[name="studentperiods-action"]').val(periodIdString);
    }

    function handleStudentDeleteClick() {
        const studentId = $(this).data('student_id');
        $('span[name="item-label"]').text("student");
        $('[name="students-action"]').val(studentId);
    }

});

