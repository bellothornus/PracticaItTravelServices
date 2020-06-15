$( document ).ready(function() {
    $('input').attr('disabled','');
    $('input').attr('readonly','');
    $('input').attr('style','background-color:white;');
    //$('input[type="checkbox"]').attr("checked", "checked");
    $('select').attr('disabled','');
    $('select').attr('readonly','');
    $('select').attr('style','background-color:white;');
    $('textarea').attr('disabled','');
    $('textarea').attr('readonly','');
    $('textarea').attr('style','background-color:white;');
    //para ocultar el arhivo en el show
    $('#id_Archivo').parent().parent().hide()
});