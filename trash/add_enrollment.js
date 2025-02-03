function initializeTable() {
    var table = $('#main-table').DataTable({
        "columnDefs": [{ "orderable": false, "targets": [0] }],
        "order": [[1, 'asc']],
        "scrollCollapse": true,
        "scrollY": '400px'
    });

    return table;
}

$(document).ready(function() {
    initializeTable();
});