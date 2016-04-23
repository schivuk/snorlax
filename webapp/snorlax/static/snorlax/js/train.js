console.log("Train.JS loaded.")

const BACK_LABEL = "back";
const FRONT_LABEL = "front";
const LEFT_LABEL = "left";
const RIGHT_LABEL = "right";

var backBtn = document.getElementById("train-back");
var frontBtn = document.getElementById("train-front");
var leftBtn = document.getElementById("train-left");
var rightBtn = document.getElementById("train-right");

backBtn.addEventListener("click", function() {
	logPosition(backBtn, BACK_LABEL);
});

frontBtn.addEventListener("click", function() {
	logPosition(frontBtn, FRONT_LABEL);
});

leftBtn.addEventListener("click", function() {
	logPosition(leftBtn, LEFT_LABEL);
});

rightBtn.addEventListener("click", function() {
	logPosition(rightBtn, RIGHT_LABEL);
});

function logPosition(button, label) {
	console.log("got callback for " + label + ", sending AJAX");
	
	$.ajax({
	    url: "/trainCurrentPosition/" + label,
	    dataType : "text",
	    async: true,
	    success: function(response) {
	    	console.log("Got ajax response: " + response)

	    	if(response == 'Success') {
	    		console.log("Success occurred.");	
	    	} else {
	    		console.log("Failure occurred");
	    	}
	        
	    },

	    error: function(jqXHR, textStatus, errorThrown) {
	    	console.log("AJAX Error occurred");
	    }
	});
}

