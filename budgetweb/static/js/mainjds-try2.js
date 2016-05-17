$(document).ready(function() {

    alert ($("#structlev1").find('option:selected').val());
    if($("#structlev1").find('option:selected').val() == 0) {
        $("#structlev2").attr('disabled',true);
    }


    //AJAX POST
     $('#structlev1').change(function(){

        alert("changing structlev1.2");
        $.ajax({
            url : "/ajax/add",
            type:'POST',
            dataType: 'json',
            success: function(data) {
                $('#structlev2').hide();
                $.each(response,function(key, value)
                {
                    $("#structlev2").append('<option value=' + key + '>' + value + '</option>');
                });
             }
        });
      });
  })





    // CSRF code


