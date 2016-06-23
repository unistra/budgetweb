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
           }

function populateselect3(){
        thechoice=$("#structlev2").find('option:selected').val();
        mychoices=thechoice.split("-----")
        mychoice=mychoices[0]
        $.ajax({
            url : "/ajax/ajax_findstruct_lev3/"+mychoice+"/",
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
                    $("#structlev3").append('<option value=' + monsplit[0] + '>' + mylabel + '</option>');
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
}


function populatecptdeplev1(){
        thechoice=$("#plfi").find('option:selected').val();
        mychoices=thechoice.split("-----")
        mychoice=mychoices[0]

        thechosenenveloppe=$("#cptdeplev1type").find('option:selected').val();

        $.ajax({
            url : "/ajax/ajax_add_enveloppe_depense/"+mychoice+"/"+thechosenenveloppe+"/",
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
                    $("#cptdeplev1").append('<option value=' + monsplit[0] + '>' + mylabel + '</option>');
                }
           }})
}


function populatecptdeplev1type(){
        thechoice=$("#plfi").find('option:selected').val();
        mychoices=thechoice.split("-----")
        mychoice=mychoices[0]
        $.ajax({
            url : "/ajax/ajax_add_enveloppetype_depense/"+mychoice+"/",
            type:'GET',
            success: function(data) {
                $("#cptdeplev1").html('');
                $("#cptdeplev1type").html('');
                $("#displaycompte").html('');

                for( i = 0; i<data.length;i++){
                    if ( i==0 ) {$("#cptdeplev1type").append('<option value=' + data[i] + ' selected >' + data[i] + '</option>');}
                           else {$("#cptdeplev1type").append('<option value=' + data[i] + '>' + data[i] + '</option>');}
                }
           }})
}


function changingdecalagetresocpae(){
        thechoice=$("#cptdeplev1").find('option:selected').val();
        $.ajax({
            url : "/ajax/ajax_get_enveloppe_decalage/"+thechoice+"/",
            type:'GET',
            success: function(data) {
                $("#decalagetresocpae").html('');
    
                if ( data[0] == "False" ) {
                    $("#decalagetresocpae").html('');
                    $("#decalagetresocpae").append('<option value="Oui"> Oui </option>');
                    $("#decalagetresocpae").append('<option value="Non" selected="selected"> Non </option>');
                    alert("Le décalage de trésorerie n'est pas autorisé pour cette nature comptable !")
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
    populatecptdeplev1type
    populatecptdeplev1
    //AJAX GET

     $('#decalagetresocpae').change(
                 changingdecalagetresocpae
             )

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

     $('#plfi').trigger("change")
     $('#cptdeplev1type').trigger("change")
     $('#cptdeplev1').trigger("change")

    // CSRF code

  // FIN DU READY
})


