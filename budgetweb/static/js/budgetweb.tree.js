jQuery(document).ready(function($) {

    function unique(value, index, arr) {
        return arr.indexOf(value) === index;
    }

    function getOpenStructures() {
        return JSON.parse(localStorage.getItem("open_structures") || "[]");
    }

    function setOpenStructures(open_structures) {
        localStorage.setItem("open_structures", JSON.stringify(open_structures));
    }

    function removeOpenStructure(open_structures, code) {
        index = open_structures.indexOf(code);
        if (index != -1) {
            open_structures.splice(index, 1);
        }
        return open_structures;
    }

    function loadChildrenCF(cf, elt) {
        $.ajax({
            url : window.location.href + cf + "/", // the endpoint,commonly same url
            type : "GET", // http method
            data : {}, // data sent with the post request
            async: false,
            // handle a successful response
            success : function(json) {
                var $ul_cf = $("#" + cf);
                // Get the parent span for the structures loaded from localStorage
                elt = (typeof elt !== 'undefined' ? elt : $ul_cf.siblings("div").children("span.cf"));
                elt.attr('title', 'Fermer cette branche').find(' > i').addClass('glyphicon-minus').removeClass('glyphicon-plus');
                $ul_cf.empty().append(json);

                // Add the cf to localStorage
                var openStructures = getOpenStructures();
                openStructures.push(cf);
                // Add an unique structure code
                openStructures = openStructures.filter(unique);
                setOpenStructures(openStructures);
            },
            // handle a non-successful response
            error : function(xhr, errmsg, err) {
                var $ul_cf = $("#" + cf);
                $ul_cf.empty().addClass("errorlist").append("Une erreur empêche la liste des centres financiers de s'afficher");
            }
        });
    }

    function loadSessionCF() {
        // var open_structures = ['ETAB'];//, 'ECP1', 'ECP', 'PAIE'];
        var openStructures = getOpenStructures();

        for(var i = 0; i < openStructures.length; i++) {
            loadChildrenCF(openStructures[i]);
        }

    }

    // Open the CF stored in localStorage
    loadSessionCF();

    $('.tree li:has(ul)').addClass('parent_li');
    $('span.cf').unbind('click');
    $('.tree li.parent_li').on('click', 'span.cf', function (e) {
        var $this = $(this);
        var children = $this.parent('div').parent('li.parent_li').find('> ul li');
        var struct_code = $this.attr('structcode');
        if (children.is(":visible")) {
            children.hide('fast');
            $this.attr('title', 'Ouvrir cette branche').find(' > i').addClass('glyphicon-plus').removeClass('glyphicon-minus');

            // Remove the closed CF and its children from localStorage
            var open_structures = getOpenStructures();
            removeOpenStructure(open_structures, struct_code);
            $.each(children.find("[structcode]"), function(index) {
                removeOpenStructure(open_structures, $(this).attr('structcode'));
            });
            setOpenStructures(open_structures);
        } else {
            children.show('fast');
            loadChildrenCF(struct_code, $this);
        }
        e.stopPropagation();
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
