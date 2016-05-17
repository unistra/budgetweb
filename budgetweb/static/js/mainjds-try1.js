$(document).ready(function() {
    alert ("entering ajax");
    if($("#structlev1").find('option:selected').val() == 0) {
        $("#structlev2").attr('disabled',true);
    }

    //AJAX GET
    $('.structlev1').change(function(){
       alert("changing structlev 1.1")
        $.ajax({
            type: "GET",
            url: "/ajax/more/",
            success: function(data) {
            for(i = 0; i< data.length;i++){
                  $('ul').append('<li>'+data[i]+'</li>');
            }
         }
         });

     });


    //AJAX POST
     $('.structlev1').change(function(){

        alert("changing structlev1.2")
        $.ajax({
            url : "/ajax/add",
            type:'POST',
            dataType: 'json',
            success: function(data) {
                $("#structlev2").attr('disabled', false);
                $.each(response,function(key, value)
                {
                    $("#structlev2").append('<option value=' + key + '>' + value + '</option>');
                });
             }
        });



         $.ajax({
             type: "POST",
             url: "/ajax/add/",
             datatype: "json",
             data: { "item": $(.todo-item").val() },
             success: function(data) {
                  alert(data.message);
            }
          });
      });




    // CSRF code


