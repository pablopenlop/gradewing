$(document).ready(function() {

    var selectedIds = new Set();
    var selectedItems = new Map();

    bindEvents();
    updateBar();
    displaySelection();

    function bindEvents() {
        $(document).on('click', '[name="row-element"]', handleRowClick);
        $(document).on('change', '[name="row-checkbox"]', handleRowCheckboxChange);
        $(document).on('change', '[name="header-checkbox"]', handleHeaderCheckboxChange);
        $(document).on('click', '#cancel-selection', handleCancelSelection);
        $(document).on('page.dt order.dt search.dt draw.dt', '#table-element', handleTableChange);
    }

    function handleRowClick() {
        
        var id = $(this).data("id");
        var checkbox = $("#row-checkbox-" + id);
        $(this).toggleClass('table-active');
        checkbox.prop('checked', !checkbox.prop('checked'));
        updateItemsByRow(checkbox);
        updateBar();
        displaySelection();
    }

    function handleCancelSelection() {
        uncheckAll();
        updateBar();
        displaySelection();
    }

    function handleRowCheckboxChange() {
        $(this).toggleClass('table-active');
        $(this).prop('checked', !$(this).prop('checked'));
        updateItemsByRow(this);
        updateBar();
        displaySelection();
    }

    function handleHeaderCheckboxChange() {
        updateItemsByHeader($(this).prop('checked'));
        updateBar();
        displaySelection();
    }

    function updateItemsByHeader(isChecked) {
        $('input[name="row-checkbox"]').each(function() {
            const value = $(this).val();
            const item = $("#cell-"+(value)).text();
            if (isChecked) {
                selectedIds.add(value);
                selectedItems.set(value, item);
                $("#row-element-" + value).addClass('table-active');
            } else {
                selectedIds.delete(value);
                selectedItems.delete(value);
                $("#row-element-" + value).removeClass('table-active');
            }
            $(this).prop('checked', isChecked);
        });
        
    }

    function updateItemsByRow(element) {
        const value = $(element).val();
        const item = $("#cell-"+(value)).text();
        if ($(element).prop('checked')) {
            selectedIds.add(value);
            selectedItems.set(value, item);
        } else {
            selectedIds.delete(value);
            selectedItems.delete(value);
            $('[name="header-checkbox"]').prop('checked', false);      
        }
    }

    function updateBar() {
        const count = selectedIds.size;
        const text = count === 1 ? "student" : "students";
        $('span[name="item-label"]').text(text);
        $('#itemCount').text(count);
        if (count > 0){
            $('#period_id').prop('disabled', true); 
            $('#optionsBar').show();
            $('#utilityBar').hide();
            $('button[name="options-button"]').prop('disabled', false); 
        } else {
            $('#period_id').prop('disabled', false); 
            $('#optionsBar').hide();
            $('#utilityBar').show();
            $('button[name="options-button"]').prop('disabled', true); 
        }
    }

    function uncheckAll() {
        selectedIds.clear();
        selectedItems.clear();
        $('#table-element').DataTable().rows().every(function() {
            var row = this.node();
            $(row).removeClass('table-active');
            $(row).find('input[name="row-checkbox"]').prop('checked', false);
        });
        $('[name="header-checkbox"]').prop('checked', false);
    }

    function handleTableChange() {
        $('[name="header-checkbox"]').prop('checked', false);
        $('input[name="row-checkbox"]').each(function() {
            const value = $(this).val();
            $(this).prop('checked', selectedIds.has(value));
        });
        $('[name="row-element"]').each(function() {
            const value = $(this).val();
            if (selectedIds.has(value)) {
                $(this).addClass('active');
            } else {
                $(this).removeClass('active');
            }
        });
    }

    function displaySelection() {
        var $ul = $('ul[name="selection-list"]');
        $ul.empty();
        selectedItems.forEach(function(value, key) {
            var $li = $('<li class="list-group-item"></li>').html('&nbsp;&nbsp;' + value);
            $ul.append($li);
        });
    }
});

