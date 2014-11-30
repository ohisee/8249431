/*$("#header").append();
$("#main").append(function () {
	return (299792458 * 100) / (1000000000);
});*/

//$("#main").append(function () {
//	return "U" + "audacity".slice(2);
//});


var bio = {
	"name" : "W.E.",
	"role" : "Software Developer",
	"contact" : {
		"email" : "developer@contact.com"
	},
	"url" : "images/fry.jpg",
	"message" : "Welcome",
	"skills" : [ "Application Design", "Software Developement" ],
	"work" : {
		"position" : "Software Developer",
		"employer" : "Org",
		"start" : "July 1st",
		"dates" : "July 1 to Present",
		"description" : "Software Developer"
	},
	"education" : {
		"start" : "July 1st",
		"name" : "CSU",
		"degree" : "BS",
		"major" : "CS",
		"location" : "SF"
	},
	"project" : {
		
	}
};

var work = {
	"position" : "Software Developer",
	"employer" : "Org",
	"start" : "July 1st",
	"dates" : "July 1 to Present",
	"description" : "Software Developer"
};

var education = {
	"start" : "July 1st",
	"name" : "CSU",
	"degree" : "BS",
	"major" : "CS",
	"location" : "SF"
};

var formattedName = HTMLheaderName.replace("%data%", bio.name);
var formattedRole = HTMLheaderRole.replace("%data%", bio.role);
var formattedContact = HTMLemail.replace("%data%", bio.contact.email);
var pic = HTMLbioPic.replace("%data%", bio.url);
var formattedWelcomeMsg = HTMLWelcomeMsg.replace("%data%", bio.message);

$("#header").prepend(formattedWelcomeMsg);
$("#header").prepend(pic);
$("#header").prepend(formattedContact);
$("#header").prepend(formattedRole);
$("#header").prepend(formattedName);

$("#workExperience").append(HTMLworkStart);
$("#workExperience").append(HTMLworkEmployer.replace("%data%", work.employer));

$("#education").append(HTMLschoolStart);
$("#education").append(HTMLschoolName.replace("%data%", education.name));
$("#education").append(HTMLschoolMajor.replace("%data%", education.major));

$(document).click(function (loc) {
	logClicks(loc.pageX, loc.pageY);
});

function inName(name) {
	var names = name.trim().split(" ");
	return names[0][0].toUpperCase() + names[0].slice(1).toLowerCase() + " "
			+ names[1].toUpperCase();
};

$("#main").append(internationalizeButton);

project.display = function() {
	$("#projects").append(HTMLprojectStart);
};

$("#mapDiv").append(googleMap);