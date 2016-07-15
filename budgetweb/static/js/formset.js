$('#add_form').click(function() {
    add_form();
});

function add_form() {
    var totalForms = $('#id_form-TOTAL_FORMS').val();
    //var maxForms = $('#id_form-MAX_NUM_FORMS').val();
    //var minForms = $('#id_form-MIN_NUM_FORMS').val();
    //var initialForms = $('#id_form-INITIAL_FORMS').val();

    var $last_row = $("#supertable tr:last");
    var $el = $last_row.clone(false);
    $el.find(":input").each(function() {
    	var name = $(this).attr('name').replace('-' + (totalForms-1) + '-','-' + totalForms + '-');
    	var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    totalForms++;
    $('#id_form-TOTAL_FORMS').val(totalForms);
    $last_row.after($el);
};