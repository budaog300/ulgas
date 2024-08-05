$(document).ready(function(){

    $('#entityType').change(function(){
        var entityType = $(this).val();
        if (entityType === 'legal'){
            $('#legalFields').show();
            $('#legalFieldsSecond').show();
            $('#legalFields input').prop('required', true);
            $('#legalFieldsSecond input').prop('required', true);

            $('individualFields').hide();
        }else {
            $('#legalFields').hide();
            $('#legalFieldsSecond').hide();
            $('#legalFields input').prop('required', false);
            $('#legalFieldsSecond input').prop('required', false);

            $('individualFields').show();
        }
    });
    $('#legalFields').hide();
    $('#legalFieldsSecond').hide();
});
