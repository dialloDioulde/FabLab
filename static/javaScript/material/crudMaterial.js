$(document).ready(function(){
    $('.show-form').click(function(){
        $.ajax({
            url: 'ajaxCreateMaterial',
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modalMaterial').modal('show');
            },
            success: function(data){
                $('#modalMaterial .modal-content').html(data.create_material);
            }
        });
    });

});