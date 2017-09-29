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

    // NatureComptable choice fields in RecetteForm and DepenseForm
    $("#supertable").on("change", ".form-enveloppe", function (e) {
        var idRegex = /id_form-(\d+).*/;
        var form_id = idRegex.exec(this.id)[1];
        var pfi_id = $("#id_form-" + form_id + "-pfi").attr("value");
        var models = ["naturecomptablerecette", "naturecomptabledepense"];
        for (var i=0; i < models.length; i++) {
            var model = models[i];
            var $nature = $("#id_form-" + form_id + "-" + model);
            if ($nature.length) {
                break;
            }
        }

        changeOptions("/api/"+ model +"/enveloppe/" + this.value + "/"+ pfi_id + "/", $nature);
    });

    // NatureComptableDetails choice fields in RecetteForm and DepenseForm
    $("#supertable").on("change", ".form-naturecomptable", function (e) {
        var idRegex = /id_form-(\d+).*/;
        var form_id = idRegex.exec(this.id)[1];
        var models = ["naturecomptablerecette", "naturecomptabledepense"];
        for (var i=0; i < models.length; i++) {
            var model = models[i];
            var $nature = $("#id_form-" + form_id + "-" + model);
            if ($nature.length) {
                break;
            }
        }
        loadDetails("/api/"+ model + "/" + $nature.val() + "/", $nature);
    });

    $('#modalMontantDC').on('show.bs.modal', function(e) {
       $("#result").empty();
       $('#txtMontantDCOrigin').empty().val($(e.relatedTarget).data('value'));
       $('#txtMontantDC').empty().val($(e.relatedTarget).data('value'));
       $('#type').empty().val($(e.relatedTarget).data('type'));
       $('#pk').empty().val($(e.relatedTarget).data('pk'));
    });

    $('#modal-submitMontantDC').on('click', function(e) {
      e.preventDefault();
      pk = $('input[name=pk]').val();
      type = $('input[name=type]').val();
      montant = $('input[name=txtMontantDC]').val();
      $.ajax({
        url : "/api/updateMontantDC/",
        type : "get",
        data : { pk : pk,
                 type : type,
                 montant : montant },
       success : function(json) {
           function reload_page(){
             window.location.reload();
           };
           $("#result").html('<div class="alert alert-success" role="alert">' + json.message + '</div>');
           window.setTimeout( reload_page, 500 );
      },
      error : function(xhr,errmsg,err) {
        $("#result").html('<div class="alert alert-danger" role="alert">' + xhr.status + ": " + xhr.responseText + '</div>');
      }
      });
      return true;
    });

    $('#modal_commentaire').on('show.bs.modal', function(e) {
       $('#modal-commentaire-field').empty().val($(e.relatedTarget).data('formid'));
    });
    $('#modal_lienpiecejointe').on('show.bs.modal', function(e) {
       $('#modal-lienpiecejointe-field').empty().append($(e.relatedTarget).data('formid'));
    });

    function loadDetails(url, dest) {
      $.getJSON(url, function(data) {
  			dest.nextAll().empty();
        if ( data.code_fonds)
          // Cas d'une recette
          dest.after("<span><br />Compte budgétaire : " + data.code_compte_budgetaire + "-" + data.label_compte_budgetaire + "<br />Fonds : " + data.code_fonds + "-" + data.label_fonds + "</span>");
        else
  			   dest.after("<span><br />Compte budgétaire : " + data.code_compte_budgetaire + "-" + data.label_compte_budgetaire + "</span>");
      });
    };

    function changeOptions(url, dest) {
        $.getJSON(url, function(data) {
            dest.empty();
            appendOptions(dest, '', '---------')
            $.each(data, function(index, obj) {
                appendOptions(dest, obj.id, obj.label);
            });
            dest.focus();
        });
    };

    function appendOptions(parent, value, html) {
        $('<option/>', {
            'value': value,
            'html': html
        }).appendTo(parent);
    };
    $('[data-toggle="tooltip"]').tooltip();
});
