$(document).ready(function() {

    const modalElement = document.getElementById('form-modal');

    delayLoading('#details-card-container');
    delayLoading('#fields-card-container');
    delayLoading('#targets-card-container');
    
    $(document).on('submit', '#checkpoint-preform-2', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                if (response.success) {
                    htmx.trigger('#details-card-container', 'refresh');
                    delayLoading('#details-card-container');
                    $('#form-modal').modal('hide');
                } else {
                    form.find('.alert').find('span').text(response.error_message);
                    form.find('.alert').show();
                    var submitButton = form.find('button[type="submit"]');
                    submitButton.prop('disabled', true);
                }
            },
            error: function(xhr, status, error) {
                $('#form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#checkpointfield-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        disableFormButtons(form);
        allowEscModal(modalElement, false);

        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                if (response.success) {
                    htmx.trigger('#fields-card-container', 'refresh');
                    delayLoading('#fields-card-container');
                    allowEscModal(modalElement, true);
                    $('#form-modal').modal('hide');
                    
                } else {
                    allowEscModal(modalElement, true);
                    restoreFormButtons(form);
                    form.find('.alert').find('span').text(response.error_message);
                    form.find('.alert').show();
                    var submitButton = form.find('button[type="submit"]');
                    submitButton.prop('disabled', true);
                }
            },
            error: function(xhr, status, error) {
                allowEscModal(modalElement, true);
                $('#form-modal').modal('hide');
                $('#error-modal').modal('show');
                
            }
        });
        
    });

    $(document).on('submit', '#checkpoint-yeargroup-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        disableFormButtons(form);
        allowEscModal(modalElement, false);
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                delayLoading('#targets-card-container');
                delayLoading('#fields-card-container');
                delayLoading('#details-card-container');
                htmx.trigger('#targets-card-container', 'refresh');
                allowEscModal(modalElement, true)
                $('#form-modal').modal('hide');
            },
            error: function(xhr, status, error) {
                allowEscModal(modalElement, true)
                $('#form-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
        

    });



    $(document).on('submit', '#delete-checkpointfield-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                delayLoading('#fields-card-container');
                htmx.trigger('#fields-card-container', 'refresh');
                $('#field-delete-modal').modal('hide');
            },
            error: function(xhr, status, error) {
                $('#field-delete-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    $(document).on('submit', '#checkpoint-yeargroup-delete-form', function(event) {
        event.preventDefault(); 
        var form = $(this)
        var formData = form.serialize(); 
        $.ajax({
            url: form.attr('action'), 
            type: 'POST', 
            data: formData, 
            success: function(response) {
                delayLoading('#fields-card-container');
                delayLoading('#details-card-container');
                delayLoading('#targets-card-container');
                htmx.trigger('#targets-card-container', 'refresh');
                $('#delete-modal').modal('hide');
            },
            error: function(xhr, status, error) {
                $('#delete-modal').modal('hide');
                $('#error-modal').modal('show');
            }
        });
    });

    function disableFormButtons(form) {
        var submitButton = form.find('button[type="submit"]');
        var cancelButton = form.find('button[type="button"]');
    
        // Disable submit button and show spinner
        submitButton.data('original-html', submitButton.html());
        submitButton.prop('disabled', true)
            .css('pointer-events', 'none')
            .html(`
                <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
                <span role="status">Saving...</span>
            `);
        // Disable cancel button
        cancelButton.prop('disabled', true);
    }


    function allowEscModal(modalElement, state){
        var modalInstance = bootstrap.Modal.getInstance(modalElement);
        modalInstance._config.keyboard = state;
    }

    function restoreFormButtons(form) {
        var submitButton = form.find('button[type="submit"]');
        var cancelButton = form.find('button[type="button"]');
    
        // Restore original HTML content
        var originalHtml = submitButton.data('original-html'); 
        submitButton.prop('disabled', false)
            .css('pointer-events', '')
            .html(originalHtml);
    
        // Enable cancel button
        cancelButton.prop('disabled', false);
    }






    // Handle individual assign/unassign
    $(document).on('click', '.individual-assign', function (e) {
        e.preventDefault();
        let newStatus = $(this).data('status') === 'on';
        let button = $(this).closest('.dropdown').find('.student-toggle');
        let cell = button.closest('td');
        let table = $(this).closest('table').DataTable(); 
        
        let row = table.row(button.closest('tr'));
        let rowData = row.data();
        console.log('clicked {{ cpyg_id }}')
        if (rowData) {
            rowData.is_active = newStatus;
    
            // Update icons 
            button.html(newStatus ? '<i class="fa-solid fa-toggle-on"></i>' 
            : '<i class="fa-solid fa-toggle-off"></i>');
            cell.attr('data-order', newStatus ? 1 : 0); 
            
            // Mark row for redraw without full reload
            row.data(rowData).invalidate(); 

            // Send AJAX POST request
            $.ajax({
                url: rowData.url_update,
                type: 'POST',
                data: JSON.stringify({ target_id: rowData.id, status: newStatus }), 
                contentType: 'application/json',
                headers: { 'X-CSRFToken': getCsrfToken() }, 
                success: function(response) {
                    console.log('post {{ cpyg_id }}')
                },
                error: function(xhr, status, error) {
                    $('#error-modal').modal('show');
                }
            });
      
        }
    
    });

    // Handle group assign/unassign
    $(document).on('click', '.group-assign', function (e) {
        e.preventDefault();
        let groupData = $(this).data('group');
        let newStatus = $(this).data('status') === 'on';
        console.log('click group')
        let table = $(this).closest('table').DataTable(); 
        let tableId = $(table.table().node()).attr('id'); 
        let dataSrc = table.settings().init().rowGroup.dataSrc;
        table.rows().every(function () {
            let rowData = this.data();
            
            if (rowData[dataSrc] === groupData) {
                rowData.is_active = newStatus; 

                let rowNode = this.node();
                if (rowNode) {
                    let cell = $(rowNode).find('td:last');
                    let button = cell.find('.student-toggle');
                    button.html(newStatus ? '<i class="fa-solid fa-toggle-on"></i>'
                    : '<i class="fa-solid fa-toggle-off"></i>');
                }
                this.data(rowData).invalidate();
            }
        });
    
        /// Send a single AJAX request
        let firstRow = table.rows().data().toArray().find(
            row => row[dataSrc] === groupData);

        if (firstRow) {
            let groupId = firstRow.group_id; 
            let url_update = firstRow.url_update; 

            $.ajax({
                url: url_update,
                type: 'POST',
                data: JSON.stringify({ 
                    grouped_target_id: groupId,  
                    status: newStatus
                }), 
                contentType: 'application/json',
                headers: { 'X-CSRFToken': getCsrfToken() },
                success: function (response) {
                    console.log('group post')
                },
                error: function (xhr, status, error) {
                    $('#error-modal').modal('show');
                }
            });
        }
    });


    


});

