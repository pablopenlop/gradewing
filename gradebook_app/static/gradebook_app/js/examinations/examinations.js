$(document).ready(function() {
});


$(document).on('click', '[name="qer-delete-btn"]', function(){
    var qer_id = $(this).val(); 
    $("#delete-qer-id").val(qer_id); 
});

$(document).on('click', '[name="cer-delete-btn"]', function(){
    var cer_id = $(this).val(); 
    $("#delete-cer-id").val(cer_id); 
});