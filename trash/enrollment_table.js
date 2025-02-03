
//register_app/js/enrollment_table.js
function tableHandler(singularLabel, pluralLabel) {
    var table = $('#table').DataTable({
        "columnDefs": [
        { "orderable": false, "targets": [0] }, 
        ],
        "order": [[1, 'asc']],
        "scrollCollapse": true,
        "scrollY": '400px'
    });
    $('[name="row-container"]').on('click', function() {

        var id = $(this).data("id");
        var checkbox = $("#row-selector-" + id);
        $(this).toggleClass('table-active');
        checkbox.prop('checked', !checkbox.prop('checked'));
        toggleItemSelection(checkbox);

    });

    var selectedItems = new Set();

    function updateLabels() {
        const count = selectedItems.size;
        const text = count === 1 ? singularLabel : pluralLabel;
        $('span[name="item-label"]').text(text);
    }

    function updateBar() {
        const count = selectedItems.size;
        updateLabels();
        $('#itemCount').text(count);

        if (count > 0) {
            $('#optionsBar').show();
            $('#utilityBar').hide();
            $('button[name="options-button"]').prop('disabled', true); // Enable buttons when count > 0
        } else {
            $('#optionsBar').hide();
            $('#utilityBar').show();
            $('button[name="options-button"]').prop('disabled', false); // Disable buttons when count is 0
        }
    }

    function toggleSelectAll(isChecked) {
        $('input[name="row-selector"]').each(function() {
            const value = $(this).val();
            if (isChecked) {
                selectedItems.add(value);
                $("#row-container-" + value).addClass('table-active');
                
            } else {
                selectedItems.delete(value);
                $("#row-container-" + value).removeClass('table-active');
            }
            $(this).prop('checked', isChecked);
            
        });
        updateBar();
        
    }

    function toggleItemSelection(element) {
        const value = $(element).val();
        if ($(element).prop('checked')) {
            selectedItems.add(value);
        } else {
            selectedItems.delete(value);
        }
        updateBar();
    }

    function uncheckAll() {
        selectedItems.clear();
        table.rows().every(function() {
            var row = this.node();
            $(row).removeClass('table-active');
            $(row).find('input[name="row-selector"]').prop('checked', false);
        });
        $('#selectAll').prop('checked', false);
        updateBar();
    }

    function pushSelectedIds() {
        var selectedIds = Array.from(selectedItems).join(',');
        $('#confirmDelete').val(selectedIds);
    }

    // Event Handlers
    $('#selectAll').change(function() {
        toggleSelectAll($(this).prop('checked'));
    });

    $(document).on('change', 'input[name="row-selector"]', function() {
        $(this).toggleClass('table-active');
        $(this).prop('checked', !$(this).prop('checked'));
        toggleItemSelection(this);
        //$(this).toggleClass('table-active');
    });

    table.on('page order search draw', function() {
        $('#selectAll').prop('checked', false);
        $('input[name="row-selector"]').each(function() {
            const value = $(this).val();
            $(this).prop('checked', selectedItems.has(value));
        });
    });

    // Cancel selected items
    $('#cancelSelection').click(function() {
        uncheckAll();
        $('#optionsBar').hide();
        $('#utilityBar').show();
    });

    // Delete selected items
    $('#deleteSelected').click(function() {
        pushSelectedIds();
    });

    // Single item delete
    $(document).on('click', '.dropdown-item[name="item-delete"]', function() {
        const value = $(this).data('id');
        selectedItems.add(value);
        updateLabels();
        pushSelectedIds();
        selectedItems.clear();
    });

    // Initial count update
    updateBar();
}


