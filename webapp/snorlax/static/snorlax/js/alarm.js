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

 function togglePosition(pos) {
    switch (pos) {
        case 1:
            //Front
            var isOn = $('#toggle-front').prop('checked');
            break;
        case 2:
            //Back
            var isOn = $('#toggle-back').prop('checked');
            break;
        case 3:
            //Right
            var isOn = $('#toggle-right').prop('checked');
            break;
        case 4:
            //Left
            var isOn = $('#toggle-left').prop('checked');
            break;
    };

    $.ajax({
        url : '/storePosBuzz',
        dataType : "html",
        type: 'POST',
        data : {
            pos: pos,
            isOn: isOn
        },
        success: function( comments ) {
            console.log('success toggling position buzzer');
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
