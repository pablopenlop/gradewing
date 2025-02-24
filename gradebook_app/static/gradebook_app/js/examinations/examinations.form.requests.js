$(document).ready(function() {

    $(document).on(
        'submit', 
        '#linear-qualification-exam-result-form, \
        #modular-qualification-exam-result-form, \
        #modular-component-exam-result-form', 
        function(event) {
            event.preventDefault(); 
            var form = $(this)
            var formData = form.serialize(); 
            $.ajax({
                url: form.attr('action'), 
                type: 'POST', 
                data: formData, 
                success: function(response) {
                    if (response.success) {
                        $('#linear-qualification-exam-result-form-modal').modal('hide');
                        $('#modular-qualification-exam-result-form-modal').modal('hide');
                        $('#modular-component-exam-result-form-modal').modal('hide');
                        if (response.update_table) {
                            updateTable(response)
                        }
                        refreshInfocard()
                    } else {
                        showAlert(form, response.error_message)
                    }
                },
                error: function(xhr, status, error) {
                    $('#linear-qualification-exam-result-form-modal').modal('hide');
                    $('#modular-qualification-exam-result-form-modal').modal('hide');
                    $('#error-modal').modal('show');
                }
            });
        }
    );

    $(document).on('submit', 
        '#qualification-exam-result-delete-form, #component-exam-result-delete-form', 
        function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                $('#delete-modal').modal('hide');
                if (response.update_table) {
                    updateTable(response)
                }
                refreshInfocard()
            },
            error: function(xhr, status, error) {
                $('#delete-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });


    function refreshInfocard(){
        let table = $('#examinations-table').DataTable();
        let selectedRow = table.row({ selected: true });
        if (selectedRow.any()) {  
            selectedRow.node().click();
        }
    }

    function updateTable(response){
        let table = $('#examinations-table').DataTable();
        let selectedRow = table.row({ selected: true });

        if (selectedRow.any()) {  
            let rowData = selectedRow.data();
            rowData.series_year = response.series_year; 
            rowData.grade = response.grade; 
            selectedRow.data(rowData);  
        }
    }

    


});