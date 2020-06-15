$(document).ready(function() {
    href = $("#boton_eliminar").attr('href');
    $("button#trigger").click(function(){
        id = $(this).parent().parent().find("td.sorting_1").text();
        console.log(id);
        console.log("hola");
        //$("#boton_eliminar").append(id);
        
        $("#boton_eliminar").attr('href',href+id);
    });
});