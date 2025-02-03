function setRequiredSelect(selectId){
    var $dpSelect = $(selectId);
    var required = $dpSelect.prop('required');
        $dpSelect.selectize({
            sortField: '',
            onChange: function() {
                $dpSelect.prop('required',required);
            }
        });
        $dpSelect.prop('required',required);
}


function setRequired_MultipleSelec(selectId){
    var $select = $(selectId);
    var required = $select.prop('required');
    $select.selectize({
        plugins: ["remove_button"],
        delimiter: ",",
        persist: false,
        placeholder: 'Select subject areas ...',
        create: function (input) {
            return {
                value: input,
                text: input,
            };
        },
});
        $select.prop('required',required);
}