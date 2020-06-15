$( document ).ready(function() {
    inputs = $('input[required], select[required], textarea[required]');
    //texto = inputs.parent().siblings('label').text();
    inputs.parent().siblings('label').append("*");
    inputs.parent().siblings('label').attr('style','font-weight:bold;')
});