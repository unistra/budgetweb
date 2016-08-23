jQuery(document).ready(function($) {
    $('.datetimepicker').datetimepicker({
        widgetPositioning: { horizontal: 'left',
                             vertical: 'bottom',
                           },
        format:'DD/MM/YYYY',
        minDate:new Date(new Date().getFullYear() - 10, 0, 1),
        maxDate: new Date(new Date().getFullYear() + 10, 11, 31),
        locale:'fr'
    });
});