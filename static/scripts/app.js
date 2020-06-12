$(document).ready(function() {

    $('#addButton').on('click', function() {

        let color = $('#color').val();

        req = $.ajax({
            url : '/update',
            type : 'POST',
            data : { color : color }
        });

        req.done(function(data) {
            $('')
        });
    });

});