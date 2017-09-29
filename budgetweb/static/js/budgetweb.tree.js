jQuery(document).ready(function($) {

    function unique(value, index, arr) {
        return arr.indexOf(value) === index;
    }

    function getOpenStructures() {
        return JSON.parse(sessionStorage.getItem("open_structures") || "[]");
    }

    function setOpenStructures(open_structures) {
        sessionStorage.setItem("open_structures", JSON.stringify(open_structures));
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
            url : window.location.href + cf + "/",
            type : "GET",
            data : {},
            async: false, //FIXME: obsolète (https://xhr.spec.whatwg.org/#sync-warning)
            // handle a successful response
            success : function(json) {
            	var $ul_cf = $("#cf" + cf);
                // Get the parent span for the structures loaded from sessionStorage
                elt = (typeof elt !== 'undefined' ? elt : $ul_cf.siblings("div").find("span.cf"));
                elt.attr('title', 'Fermer cette branche').find(' > i').addClass('glyphicon-minus').removeClass('glyphicon-plus');
                $ul_cf.empty().append(json);

                // Add the cf to sessionStorage
                var openStructures = getOpenStructures();
                openStructures.push(cf);
                // Add an unique structure code
                openStructures = openStructures.filter(unique);
                setOpenStructures(openStructures);
            },
            // handle a non-successful response
            error : function(xhr, errmsg, err) {
                var $ul_cf = $("#cf" + cf);
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

    // Open the CF stored in sessionStorage
    loadSessionCF();

    $('.tree li:has(ul)').addClass('parent_li');
    $('span.cf').unbind('click');
    $('.tree li.parent_li').on('click', 'span.cf', function (e) {
        var $this = $(this);
        var children = $this.parent('div').closest('li.parent_li').find('> ul li');
        var struct_id = $this.attr('structid');
        if (children.is(":visible")) {
            children.hide('fast');
            $this.attr('title', 'Ouvrir cette branche').find(' > i').addClass('glyphicon-plus').removeClass('glyphicon-minus');

            // Remove the closed CF and its children from sessionStorage
            var open_structures = getOpenStructures();
            removeOpenStructure(open_structures, struct_id);
            $.each(children.find("[structid]"), function(index) {
                removeOpenStructure(open_structures, $(this).attr('structid'));
            });
            setOpenStructures(open_structures);
        } else {
            children.show('fast');
            loadChildrenCF(struct_id, $this);
        }
        e.stopPropagation();
    });
});
