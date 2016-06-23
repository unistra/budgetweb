function populateselect2(){
        mychoice=$("#structlev1").find('option:selected').val();
        $.ajax({
            url : "/ajax/ajax_recadd/"+mychoice+"/",
            type:'GET',
            success: function(data) {
                $("#structlev2").html('');
                $("#structlev3").html('');
                var monsplit;
                var mylabel;
                var myseparator;
                myseparator="-----"

                for( i = 0; i<data.length;i++){
                    monsplit = data[i].split(myseparator)
                    mylabel = monsplit[1]+myseparator+monsplit[2]

                    $("#structlev2").append('<option value=' + monsplit[0] + '>' + mylabel + '</option>');
                }
           }})
          $("#structlev2").trigger("change"); 
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
                var monsplit;
                var mylabel;
                var myseparator;
                myseparator="-----"
                for( i = 0; i<data.length;i++){
                    monsplit = data[i].split(myseparator)
                    mylabel = monsplit[1]+myseparator+monsplit[2]
                    $("#structlev3").append('<option value='  + monsplit[0] + '>' + mylabel + '</option>');
                }
           }})
          $("#structlev3").trigger("change");
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
                var monsplit;
                var mylabel;
                var myseparator;
                myseparator="-----"

                for( i = 0; i<data.length;i++){
                    monsplit = data[i].split(myseparator)
                    mylabel = monsplit[1]
                    $("#plfi").append('<option value=' + monsplit[0] + '>' + mylabel + '</option>');
                }
           }})
          $("#plfi").trigger("change");
}


function populatecptdeplev1(){
        thechoice=$("#plfi").find('option:selected').val();
        //mychoices=thechoice.split("-----")
        //mychoice=mychoices[0]
        thechosenenveloppe=$("#cptdeplev1type").find('option:selected').val();

        $.ajax({
            url : "/ajax/ajax_add_enveloppe/"+thechoice+"/"+thechosenenveloppe+"/",
            type:'GET',
            success: function(data) {
                $("#cptdeplev1").html('');
                var monsplit;
                var mylabel;
                var myseparator;
                myseparator="-----"

                for( i = 0; i<data.length;i++){
                    monsplit = data[i].split(myseparator)
                    mylabel = monsplit[1]+myseparator+monsplit[2]
                    if (i==0) {
                            $("#cptdeplev1").append('<option value=' + monsplit[0] + ' selected="selected" >' + mylabel + '</option>');
                             } else {
                            $("#cptdeplev1").append('<option value=' + monsplit[0] + '>' + mylabel + '</option>');
                         }
                }
           }})
           //$("#cptdeplev1").selectedIndex=0;
          $("#cptdeplev1").trigger("change"); 
}

function populatecptdeplev1type(){
        thechoice=$("#plfi").find('option:selected').val();
        //mychoices=thechoice.split("-----")
        //mychoice=mychoices[0]
        $("#cptdeplev1type").html('');
        $.ajax({
            url : "/ajax/ajax_add_enveloppetype/"+thechoice+"/",
            type:'GET',
            success: function(data) {
                $("#cptdeplev1type").append('<option> Choisissez une enveloppe</option>');
                for( i = 0; i<data.length;i++){
                                 $("#cptdeplev1type").append('<option value=' + data[i] + '>' + data[i] + '</option>');
                }

           }})
           $("#cptdeplev1").html('');
           $("#displaycompte").html('');
           $("#cptdeplev1type").trigger("change");
}


function displaycompte(){
        $("#displaycompte").html('');
        thechoice=$("#cptdeplev1").find('option:selected').val();
        $.ajax({
            url : "/ajax/ajax_recette_displaycompte/"+thechoice+"/",
            type:'GET',
            success: function(data) {
                $("#displaycompte").append('compte budgétaire: '+ data);
           }})
}


$(document).ready(function() {
    //alert ($("#structlev1").find('option:selected').val());
    if($("#structlev1").find('option:selected').val() == 0) {
        $("#structlev2").attr('disabled',true);
    }
    populateselect2
    populateselect3
    populatecptdeplev1type
    populatecptdeplev1

    //AJAX GET
     $('#structlev1').change(populateselect2
             )

     $('#structlev2').change(populateselect3
             )

     $('#structlev3').change(populatepfi
             )


     $('#plfi').change(populatecptdeplev1type
             )

     $('#cptdeplev1type').change(populatecptdeplev1
             )


     $('#cptdeplev1').change(displaycompte
             )

     $('#plfi').trigger("change")
     $('#cptdeplev1type').trigger("change")
     //$('#cptdeplev1').trigger("change")

    // CSRF code

  // FIN DU READY
})


