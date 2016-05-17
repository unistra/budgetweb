$(document).ready(function() {


    //alert ($("#structlev1").find('option:selected').val());
    if($("#structlev1").find('option:selected').val() == 0) {
        $("#structlev2").attr('disabled',true);
    }


    //AJAX GET
     $('#structlev1').change(function(){
        mychoice=$("#structlev1").find('option:selected').val();
        $.ajax({
            url : "/ajax/ajax_add/"+mychoice+"/",
            type:'GET',
            success: function(data) {
                $("#structlev2").html('');
                $("#structlev3").html('');
                for( i = 0; i<data.length;i++){
                    $("#structlev2").append('<option value=' + data[i] + '>' + data[i] + '</option>');
                }
           }})
             })

     $('#structlev2').change(function(){
        thechoice=$("#structlev2").find('option:selected').val();
        mychoices=thechoice.split("-----")
        mychoice=mychoices[0]
        $.ajax({
            url : "/ajax/ajax_findstruct_lev3/"+mychoice+"/",
            type:'GET',
            success: function(data) {
                $("#structlev3").html('');
                for( i = 0; i<data.length;i++){
                    $("#structlev3").append('<option value=' + data[i] + '>' + data[i] + '</option>');
                }
           }})
             })


     $('#cptdeplev1').change(function(){
        mychoice=$("#cptdeplev1").find('option:selected').val();
        $.ajax({
            url : "/ajax/ajax_add_cptdev_lev2/"+mychoice+"/",
            type:'GET',
            success: function(data) {
                $("#cptdeplev2").html('');
                for( i = 0; i<data.length;i++){
                    $("#cptdeplev2").append('<option value=' + data[i] + '>' + data[i] + '</option>');
                }
           }})
             })

     $('#orfond').change(function(){
        mychoice=$("#orfond").find('option:selected').val();
        $.ajax({
            url : "/ajax/ajax_findorigfond_lev2/"+mychoice+"/",
            type:'GET',
            success: function(data) {
                $("#orfond2").html('');
                for( i = 0; i<data.length;i++){
                    $("#orfond2").append('<option value=' + data[i] + '>' + data[i] + '</option>');
                }
           }})
             })


    // CSRF code

  // FIN DU READY
})


