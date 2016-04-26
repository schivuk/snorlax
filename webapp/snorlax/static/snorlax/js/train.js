console.log("Train.JS loaded.")

const BACK_LABEL = "back";
const FRONT_LABEL = "front";
const LEFT_LABEL = "left";
const RIGHT_LABEL = "right";
const ON = "on";
const OFF = "off";
const BUTTON_ACTIVE_CLASS = "btn btn-primary btn-lg";
const BUTTON_DISABLED_CLASS = "btn btn-primary btn-lg disabled";
const ORANGE_BUTTON_ACTIVE = "btn btn-warning btn-lg";
const ORANGE_BUTTON_DISABLED = "btn btn-warning btn-lg disabled"
const RED_BUTTON_ACTIVE = "btn btn-danger btn-lg";
const RED_BUTTON_DISABLED = "btn btn-danger btn-lg disabled";

var backBtn = document.getElementById("train-back");
var frontBtn = document.getElementById("train-front");
var leftBtn = document.getElementById("train-left");
var rightBtn = document.getElementById("train-right");
var onBtn = document.getElementById("train-on");
var offBtn = document.getElementById("train-off");
var updatePredBtn = document.getElementById("update-predictor-btn");
var numPositionsBadge = document.getElementById("num-samples-badge");
var numOnOffBadge = document.getElementById("num-onoff-badge");
var removeAllBtn = document.getElementById("remove-all-btn");

var backStatusElem = document.getElementById("back-status-elem");
var frontStatusElem = document.getElementById("front-status-elem");
var leftStatusElem = document.getElementById("left-status-elem");
var rightStatusElem = document.getElementById("right-status-elem");
var predictorStatus = document.getElementById("update-predictor-status");
var removeAllStatus = document.getElementById("remove-all-status");

var onStatusElem = document.getElementById("on-status-elem");
var offStatusElem = document.getElementById("off-status-elem");

backBtn.addEventListener("click", function() {
	logPosition(backBtn, backStatusElem, BACK_LABEL);
});

frontBtn.addEventListener("click", function() {
	logPosition(frontBtn, frontStatusElem, FRONT_LABEL);
});

leftBtn.addEventListener("click", function() {
	logPosition(leftBtn, leftStatusElem, LEFT_LABEL);
});

rightBtn.addEventListener("click", function() {
	logPosition(rightBtn, rightStatusElem, RIGHT_LABEL);
});

updateNumReadings();

onBtn.addEventListener("click", function() {
	logOnOff(onBtn, onStatusElem, ON);
});

offBtn.addEventListener("click", function() {
	logOnOff(offBtn, offStatusElem, OFF);
})

updatePredBtn.addEventListener("click", function() {
	console.log("Learning positions..");
	predictorStatus.innerHTML = "Updating predictor...";
	updatePredBtn.className = ORANGE_BUTTON_DISABLED;

	$.ajax({
	    url: "/learnPositions",
	    method: 'GET',
	    dataType : "text",
	    async: true,
	    timeout: 5000,
	    success: function(response) {
	    	console.log("Got ajax response: " + response)

	    	updatePredBtn.className = ORANGE_BUTTON_ACTIVE;
	    	if(response == 'Success') {
	    		console.log("Success occurred.");
	    		predictorStatus.innerHTML = "Success: Updated predictor";	

	    	} else {
	    		console.log("Failure occurred");
	    		predictorStatus.innerHTML = "Update failed: " + response;
	    	}
	        
	    },

	    error: function(jqXHR, textStatus, errorThrown) {
	    	updatePredBtn.className = ORANGE_BUTTON_ACTIVE;
	    	console.log("AJAX Error occurred: " + errorThrown);
	    	predictorStatus.innerHTML = "Error occurred: " + errorThrown;
	    },


	});
})

removeAllBtn.addEventListener("click", function() {
	console.log("removeAllBtn called");

	removeAllStatus.innerHTML = "Removing all samples..";
	removeAllBtn.className = RED_BUTTON_DISABLED
	$.ajax({
	    url: "/clearAll",
	    method: 'GET',
	    dataType : "text",
	    async: true,
	    timeout: 5000,
	    success: function(response) {
	    	console.log("Got ajax response: " + response)

	    	removeAllBtn.className = RED_BUTTON_ACTIVE;
	    	if(response == 'Success') {
	    		console.log("Success occurred.");
	    		removeAllStatus.innerHTML = "Success: Removed all calibration examples";	
	    		updateNumReadings();


	    	} else {
	    		console.log("Failure occurred");
	    		removeAllStatus.innerHTML = "Failed to remove calibration examples";
	    	}
	    },

	    error: function(jqXHR, textStatus, errorThrown) {
	    	removeAllBtn.className = RED_BUTTON_ACTIVE;
	    	console.log("AJAX Error occurred: " + errorThrown);
	    	removeAllStatus.innerHTML = "Error occurred removing calibration examples: " + errorThrown;
	    },
	});

});

function logPosition(button, statusElem, label) {
	console.log("got callback for " + label + ", sending AJAX");
	statusElem.innerHTML = "fetching data from bed...";
	//change button availability temporarily while call is made
	button.className = BUTTON_DISABLED_CLASS;
	$.ajax({
	    url: "/trainCurrentPosition/" + label,
	    method: 'GET',
	    dataType : "text",
	    async: true,
	    timeout: 5000,
	    success: function(response) {
	    	console.log("Got ajax response: " + response)

	    	button.className = BUTTON_ACTIVE_CLASS;
	    	if(response == 'Success') {
	    		console.log("Success occurred.");
	    		statusElem.innerHTML = "Successful log for " + label;	
	    		predictorStatus.innerHTML = "";
	    		removeAllStatus.innerHTML = "";
	    		updateNumReadings();
	    		
	    	} else {
	    		console.log("Failure occurred");
	    		statusElem.innerHTML = "Failed to log for " + label;
	    	}
	        
	    },

	    error: function(jqXHR, textStatus, errorThrown) {
	    	button.className = BUTTON_ACTIVE_CLASS;
	    	console.log("AJAX Error occurred: " + errorThrown);
	    	statusElem.innerHTML = "Error occurred: " + errorThrown;
	    },


	});
}


function logOnOff(btn, statusElem, label) {
	statusElem.innerHTML = "Logging this position...";
    btn.className = BUTTON_DISABLED_CLASS;

	$.ajax({
	    url: "/trainOnOff/" + label,
	    method: 'GET',
	    dataType : "text",
	    async: true,
	    timeout: 5000,
	    //temporarily disable button
	    success: function(response) {
	    	console.log("Got ajax response: " + response);

	    	btn.className = BUTTON_ACTIVE_CLASS;
	    	statusElem.innerHTML = "Successful train: " + label;
	    	updateNumReadings();
	    },

	    error: function(jqXHR, textStatus, errorThrown) {
	    	console.log("AJAX Error occurred in updateNumReadings: " + errorThrown);
	    	btn.className = BUTTON_ACTIVE_CLASS;
	    	statusElem.innerHTML = "Error occurred: " + errorThrown;
	    },
	});

}


//update both: num readings for positions as well as on/off
function updateNumReadings() {
	console.log("Called updateNumReadings..");

	$.ajax({
	    url: "/numReadingGroups",
	    method: 'GET',
	    dataType : "text",
	    async: true,
	    timeout: 5000,
	    success: function(response) {
	    	console.log("Got ajax response: " + response);

	    	numPositionsBadge.innerHTML = response + " samples taken";	
	    },

	    error: function(jqXHR, textStatus, errorThrown) {
	    	console.log("AJAX Error occurred in updateNumReadings: " + errorThrown);
	    	
	    },
	});

	$.ajax({
	    url: "/numOnOffSamples",
	    method: 'GET',
	    dataType : "text",
	    async: true,
	    timeout: 5000,
	    success: function(response) {
	    	console.log("Got ajax response: " + response);

	    	numOnOffBadge.innerHTML = response + " samples taken";	
	    },

	    error: function(jqXHR, textStatus, errorThrown) {
	    	console.log("AJAX Error occurred in updateNumReadings: " + errorThrown);
	    	numOnOffBadge.innerHTML = "?";
	    },
	});
}

