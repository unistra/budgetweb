function populateselect2(){
        mychoice=$("#structlev1").find('option:selected').val();
        $.ajax({
            url : "/ajax/ajax_recadd/"+mychoice+"/",
            type:'GET',
            success: function(data) {
                $("#structlev2").html('');
                $("#structlev3").html('');
                for( i = 0; i<data.length;i++){
                    $("#structlev2").append('<option value=' + data[i] + '>' + data[i] + '</option>');
                }
           }})
           }


function populateselect3(){
        thechoice=$("#structlev2").find('option:selected').val();
        mychoices=thechoice.split("-----")
        mychoice=mychoices[0]
        $.ajax({
            url : "/ajax/ajax_recfindstruct_lev3/"+mychoice+"/",
            type:'GET',
            success: function(data) {
                $("#structlev3").html('');
                for( i = 0; i<data.length;i++){
                    $("#structlev3").append('<option value=' + data[i] + '>' + data[i] + '</option>');
                }
           }})

}


function populatepfi(){
        thechoice=$("#structlev3").find('option:selected').val();
        mychoices=thechoice.split("-----")
        mychoice=mychoices[0]
        $.ajax({
            url : "/ajax/ajax_add_eotp/"+mychoice+"/",
            type:'GET',
            success: function(data) {
                $("#plfi").html('');
                for( i = 0; i<data.length;i++){
                    $("#plfi").append('<option value=' + data[i] + '>' + data[i] + '</option>');
                }
           }})
}


function populatecptdeplev1(){
        thechoice=$("#plfi").find('option:selected').val();
        mychoices=thechoice.split("-----")
        mychoice=mychoices[0]
        $.ajax({
            url : "/ajax/ajax_add_enveloppe/"+mychoice+"/",
            type:'GET',
            success: function(data) {
                $("#cptdeplev1").html('');
                for( i = 0; i<data.length;i++){
                    $("#cptdeplev1").append('<option value=' + data[i] + '>' + data[i] + '</option>');
                }
           }})
}


$(document).ready(function() {
    //alert ($("#structlev1").find('option:selected').val());
    if($("#structlev1").find('option:selected').val() == 0) {
        $("#structlev2").attr('disabled',true);
    }
    populateselect2
    populateselect3

    //AJAX GET
     $('#structlev1').change(populateselect2
             )

     $('#structlev2').change(populateselect3
             )

     $('#plfi').change(populatecptdeplev1
             )


     $('#orfond').change(function(){
        mychoice=$("#orfond").find('option:selected').val();
        $.ajax({
            url : "/ajax/ajax_recfindorigfond_lev2/"+mychoice+"/",
            type:'GET',
            success: function(data) {
                $("#orfond2").html('');
                for( i = 0; i<data.length;i++){
                    $("#orfond2").append('<option value=' + data[i] + '>' + data[i] + '</option>');
                }
           }})
             })

     $('#structlev3').change(populatepfi
             )

    // CSRF code

  // FIN DU READY
})


