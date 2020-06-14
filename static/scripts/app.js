// Set of various functions
$(document).ready(function() {

    // On update button click perform an ajax call
    $('.update-button').on('click', function() {

        // Retrieve button id from said button (attribute)
        let button_id = $(this).attr('button_id');

        // Post the data to the server
        req = $.ajax({
            url : '/update_count',
            type : 'POST',
            data : { button_id : button_id },
        });

        // Update the DOM with data recieved from the server
        req.done(function(data) {
            $('#count'+button_id).text(data.count);
        });
    });

    // Play click sound on button click
    $('.button').click(function () { 
        
        $('#click-sound')[0].play();
        
    });
    
    // Close any alert after 4 seconds
    setTimeout (function () {
        $(".alert").alert('close');
    }, 4000)

    // Disable multiplier in manual reset mode
    $('#timespan').click(function() {
        selected = $('#timespan').val();
        if (selected == "manualreset"){
            $('#multiplier').prop("disabled", true);
        } else {
            $('#multiplier').prop("disabled", false);
        }
    });
});