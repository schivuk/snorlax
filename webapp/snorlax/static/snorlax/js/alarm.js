$(function() {
    $('#toggle-two').bootstrapToggle({
      on: 'Alarm On',
      off: 'Alarm Off',
      width: '400'
    });    
});


 function toggleAlarm() {
    var isOn = $('#toggle-two').prop('checked');
    console.log(isOn);

    $.ajax({
        url : '/alarm',
        dataType : "html",
        type: 'POST',
        data : {
            isOn: isOn
        },
        success: function( comments ) {
            console.log('success toggling alarm backend');
        },

        //If an error occurred, we alert user, and log errors
        error: function(xhr, status, errorThrown) {
            alert("Encountered a Problem.");
            console.log("Error: " + errorThrown);
            console.log("Status" + status);
            console.dir(xhr);
        }
    });
 }

 function increment(field) {
    if(field === 'hour') {
        var div = $('#hour');
        var hour = parseInt(div.val());
        if(hour < 12) {
            div.val(hour+1);
        }
    } else {
        var div = $('#minute');
        var min = parseInt(div.val());
        if(min < 60) {
            div.val(min+1);
        }
    }
  }

function decrement(field) {
    if(field === 'hour') {
        var div = $('#hour');
        var hour = parseInt(div.val());
        if(hour > 0) {
            div.val(hour-1);
        }
    } else {
        var div = $('#minute');
        var min = parseInt(div.val());
        if(min > 0) {
            div.val(min-1);
        }
    }
}
