
function updateView(selectedItems){
    updateHeaderBar(selectedItems.size);
    updateStudentActions(selectedItems);
    updateStudentPeriodActions(selectedItems);
}

function updateStudentActions(selectedItems) {
    var idList = Array.from(selectedItems.keys());
    var idString = idList.join(',');
    $('[name="students-action"]').val(idString);
}

function updateStudentPeriodActions(selectedItems) {
    var periodIdList = Array.from(selectedItems.values()).map(item => item.studentPeriodId);
    var periodIdString = periodIdList.join(',');
    $('[name="studentperiods-action"]').val(periodIdString);
}

function updateHeaderBar(count) {
        const text = count === 1 ? "student" : "students";
        $('span[name="row-label"]').text(text);
        $('#row-count').text(count);
        if (count > 0){
            $('#options-bar').show();
            $('#menu-bar').hide();
        } else {
            $('#options-bar').hide();
            $('#menu-bar').show();
        }
    }

