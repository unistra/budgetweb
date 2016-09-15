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
});
