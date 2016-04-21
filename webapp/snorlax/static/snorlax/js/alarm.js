$(function() {
    $('#toggle-two').bootstrapToggle({
      on: 'Alarm On',
      off: 'Alarm Off',
      width: '400'
    });    
});

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
