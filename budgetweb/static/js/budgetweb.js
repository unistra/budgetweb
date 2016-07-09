$(document).ready(function() {
    $('.tree li:has(ul)').addClass('parent_li').find(' > span').attr('title', 'Ouvrir cette branche');
    $('span').unbind('click');
    $('.tree li.parent_li > span').on('click', function (e) {
        var children = $(this).parent('li.parent_li').find(' > ul > li');
        if (children.is(":visible")) {
            children.hide('fast');
            $(this).attr('title', 'Expand this branch').find(' > i').addClass('glyphicon-plus').removeClass('glyphicon-minus');
        } else {
            children.show('fast');
            $(this).attr('title', 'Collapse this branch').find(' > i').addClass('glyphicon-minus').removeClass('glyphicon-plus');
            cf = $(this).attr('toto');
            $.ajax({
                         url : window.location.href+"getsubtree/"+cf, // the endpoint,commonly same url
                         type : "GET", // http method
                         data : { }, // data sent with the post request
                   // handle a successful response
                   success : function(json) {

                      $("#"+cf).empty().append(json);
                  },
                  // handle a non-successful response
                  error : function(xhr,errmsg,err) {
                    //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                    remarque=document.getElementById("modal_remarque");
                    try {
                      result=JSON.parse(xhr.responseText);
                      listeErrorHTML = "";
                      $.each(result, function(k, v) {
                        //display the key and value pair
                        var msg = '<label class="TarifWebError" for="'+k+'">'+v+'</label>';
                        $('input[name="' + k + '"], select[name="' + k + '"]').not('form[name="search"]').addClass('inputTxtError').after(msg);
                      });
                      remarque.innerHTML=listeErrorHTML;
                    }
                    catch(e) {
                      // Rien a battre, on a une erreur, on s'en fou.
                    }
                  }
            });


        }
        e.stopPropagation();
    });
});
