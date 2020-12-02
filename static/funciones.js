const base = 'http://127.0.0.1:8000/';
var subtotal = 0;

async function fetchAsync(url, body, method = 'POST'){
    let response = await fetch(url,{
      method: method,
      mode: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      }
    });
    let data = await response.text();
    return data;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var eliminar_turno = function(e){
        e.preventDefault();
        if(!confirm("¿Desea eliminar el turno?")){
            return;
        }
        $.post(this.href, function(data) {
            if (data.result == "ok"){
                alert("Turno eliminado correctamente!");
                window.location=base+"listado_turnos";
            } else {
                alert("Ocurrio un error");
            }
        }).fail(function() {
            alert("error");
        });
        return false;
    }

    var obtener_datos_producto = (e) => {
        e.preventDefault();
        var precio = document.getElementById('id_unitario');
        var clasi = document.getElementById('id_clasificacion');

        $.post(base+"get_datos_producto/"+e.target.value, function(data) {
            if (data[0].id == e.target.value){
                precio.value = data[0].precio;                
                clasi.value = data[0].clasificacion;
                showOpcionesLente(data[0].clasificacion);
            } else {
                alert("Ocurrio un error");
            }
        }).fail(function() {
            alert("error");
        });
    }

    var getDetallePedido = (e) => {
        e.preventDefault();
        $.post(base+"get_detalle_pedido/"+e.target.id, function(data) {
            if (data != ''){
                $("#body_detallePedido").html(data);
                $('#modal_pedido').modal('show')
            } else {
                alert("Ocurrio un error");
            }
        }).fail(function() {
            alert("error");
        });
    }


    $(".del_turno").click(eliminar_turno);
    $("#id_producto").change(obtener_datos_producto);
    $(".detalle_pedido").click(getDetallePedido);
});

$('#id_producto').change(function(e){

});

$('#id_clasificacion').change(function(e){
    var clasif = this.value;
    showOpcionesLente(clasif);
});

function showOpcionesLente(clasif){
    var mostrar = "none";
    if(clasif == "L"){
        mostrar = "block";        
    }

    $("#id_cercania").css("display", mostrar);
    $("label[for='id_cercania']").css("display", mostrar);

    $("#id_armazon").css("display", mostrar);
    $("label[for='id_armazon']").css("display", mostrar);

    $("#id_lado").css("display", mostrar);
    $("label[for='id_lado']").css("display", mostrar);
}

$('#add_more').click(function(){
    //cloneMore('div.table:last', 'service');

    var prod = document.getElementById('id_producto');
    var cant = document.getElementById('id_cantidad');
    var precio = document.getElementById('id_unitario');
    var clasi = document.getElementById('id_clasificacion');
    var total = 0;
    var cercania = document.getElementById("id_cercania");
    var lado = document.getElementById("id_lado");
    var armazon = document.getElementById("id_armazon");

    if(prod.value == ''){
        alert("Debe seleccionar un producto!"); return;
    }

    if(cant.value == 0 || cant.value == ''){
        alert("Debe informar la cantidad!"); return;
    }

    if(precio.value == 0 || precio.value == ''){
        alert("Debe informar el precio!"); return;
    }

    if(clasi.value == 'L'){
        if(cercania.value == '' || cercania.value == '-'){
            alert("Debe informar la cercania!"); return;
        }

        if(lado.value == '' || lado.value == '-'){
            alert("Debe informar el lado!"); return;
        }

        if(armazon.value == '' || armazon.value == '-'){
            alert("Debe informar si tiene armazon!"); return;
        }
    }else{
        cercania.value = '-';
        lado.value = '-';
        armazon.value = '-';
    }
    
    var $tr = $("#tr_to_clone").closest('.tr_clone');
    var $clone = $tr.clone();
    $clone.find(':text').val('');
    $clone.find('.clsprod').val(prod.value);
    $clone.find('.clsclasi').val(clasi.value);
    $clone.find('.clslado').val(lado.value);
    $clone.find('.clscerca').val(cercania.value);
    $clone.find('.clsarma').val(armazon.value);
    $clone.find('.clsprod').val(prod.value);
    $clone.find('.clscant').val(cant.value);
    $clone.find('.clsunit').val(precio.value);
    $clone.find('.clstot').val(cant.value*precio.value);
    $tr.after($clone);

    subtotal+=(cant.value*precio.value);
    $("#subtotal").val(subtotal);

    prod.value = "";
    clasi.value = "";
    lado.value = "";
    cercania.value = "";
    armazon.value = "";
    prod.value = "";
    cant.value = "";
    precio.value = "";

});


$('#f_solicitar').click(function(e){
    e.preventDefault();

    var fd = $("#fhd").val();
    var fh = $("#fhh").val();

    if(fd == ''){
        alert("Debe informar la fecha desde");
        return;
    }

    if(fh == ''){
        alert("Debe informar la fecha hasta");
        return;
    }

    $("#f_resultados").html("<img class='img-responsive' src='https://2.bp.blogspot.com/-AEq7PhrFev0/V8uoZHZ5zOI/AAAAAAAACAY/Ck3z6Gu2hbcMPjhh7ASYeYTWItP5L2nMQCLcB/s1600/1.gif'>")
    var rep_apac = $("#f_apac");
    var rep_ipac = $("#f_ipac");
    var rep_ppac = $("#f_ppac");
    var rep_pvend = $("#f_pvend");
    var rep_vvend = $("#f_vvend");

    if(rep_apac.is(':checked')){ rep = 'apac'; }
    if(rep_ipac.is(':checked')){ rep = 'ipac'; }
    if(rep_ppac.is(':checked')){ rep = 'ppac'; }
    if(rep_pvend.is(':checked')){ rep = 'pvend'; }
    if(rep_vvend.is(':checked')){ rep = 'vvend'; }

    //window.open(base+"get_reporte/"+rep+"/"+fd+"/"+fh,'_blank');

    $.post(base+"get_reporte/"+rep+"/"+fd+"/"+fh, function(data) {
        if (data != ''){
            $("#f_resultados").html(data);
        } else {
            alert("Error");
        }
    }).fail(function() {
        alert("error");
    });
});
