console.log("Currposition.js loaded.");

//const IMG_VISIBLE_STYLE = "display:block; margin-left: auto; margin-right: auto;";
//const IMG_HIDDEN_STYLE = "visibility: hidden";
const IMG_HIDDEN_CLASS = "invisible";
const IMG_VISIBLE_CLASS = "img-fluid";
const BACK = "back";
const FRONT = "front";
const LEFT = "left";
const RIGHT = "right";
const OFF = "off";
const BACK_IMG = "/static/snorlax/img/back.png";
const FRONT_IMG = "/static/snorlax/img/belly.png";
const LEFT_IMG = "/static/snorlax/img/facing-left.png";
const RIGHT_IMG = "/static/snorlax/img/facing-right.png";
const OFF_IMG = "/static/snorlax/img/off.png";


const BUTTON_ACTIVE_CLASS = "btn btn-primary btn-lg btn-block";
const BUTTON_DISABLED_CLASS = "btn btn-primary btn-lg btn-block disabled";

//maps position to image file
var imgFileDict = new Array();
imgFileDict[FRONT] = FRONT_IMG;
imgFileDict[BACK] = BACK_IMG;
imgFileDict[LEFT] = LEFT_IMG;
imgFileDict[RIGHT] = RIGHT_IMG;
imgFileDict[OFF] = OFF_IMG;

var getPositionBtn = document.getElementById("get-position-btn");
var posStatusElem = document.getElementById("position-status");
var posImg = document.getElementById("position-img");
var onOffStatus = document.getElementById("on-off-status");


getPositionBtn.addEventListener("click", function(){
	//disable button until call is made
	getPositionBtn.className = BUTTON_DISABLED_CLASS;

	//remove earlier image
	posImg.className = IMG_HIDDEN_CLASS;
	posStatusElem.innerHTML = "Retrieving current position..."

	$.ajax({
	    url: "/getCurrentPosition",
	    method: 'GET',
	    dataType : "text",
	    async: true,
	    timeout: 5000,
	    success: function(response) {
	    	console.log("Got ajax response: " + response)

	    	getPositionBtn.className = BUTTON_ACTIVE_CLASS;
	    	if(response == OFF || response == FRONT || response == BACK || 
	    				response == LEFT || response ==RIGHT) {
	    		console.log("Success occurred.");
	    		posStatusElem.innerHTML = "Your position is: " + response;
	    		//TODO update image
	    		console.log("Setting posImg src to: " + imgFileDict[response])
	    		posImg.src = imgFileDict[response];
	    		posImg.className = IMG_VISIBLE_CLASS;

	    		if(response == OFF) {
	    			onOffStatus.innerHTML = "Off the bed";
	    		} else {
	    			onOffStatus.innerHTML = "On the bed";
	    		}
	    	} else {
	    		console.log("Failure occurred");
	    		posStatusElem.innerHTML = "Error retrieving position: " + response;
	    	}
	    },

	    error: function(jqXHR, textStatus, errorThrown) {
	    	getPositionBtn.className = BUTTON_ACTIVE_CLASS;
	    	console.log("AJAX Error occurred: " + errorThrown);
	    	posStatusElem.innerHTML = "Error occurred retrieving position: " + errorThrown;
	    },
	});
});

