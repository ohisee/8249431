/**
 * New node file
 */

var sampleArray = [0,0,7];

var incrementLastArrayElement = function(_array) {
    var newArray = _array.slice(0);
    var i = newArray[newArray.length - 1];
    newArray[newArray.length - 1] = i + 1;
    var i = newArray.pop();
    newArray.push(i + 1);
    return newArray;
};

// Did your code work? The line below will tell you!
console.log(incrementLastArrayElement(sampleArray));

var name = "AlbERt EINstEiN";

function nameChanger(oldName) {
	var finalName = oldName[0].toUpperCase()
			+ oldName.slice(1, oldName.indexOf(' ')).toLowerCase()
			+ oldName.slice(oldName.indexOf(' ')).toUpperCase();
	return finalName;
};

// Did your code work? The line below will tell you!
console.log(nameChanger(name));

var html = '<script src="http://hackyourwebsite.com/eviljavascript.js"></script>';

var charEscape = function(_html) {
    var newHTML = _html;
    // How will you make sure that newHTML doesn't contain any < or > ?
    // Your code goes here!
    newHTML = _html.replace("<", "&lt;").replace(">", "&gt;");
    // Don't delete this line!
    return newHTML;
};

// Did your code work? The line below will tell you!
console.log(charEscape(html));

//var str = 'apples are round, and apples are juicy. apples apples';
//var newstr = str.replace('apples', 'oranges', 'gi');
//console.log(newstr);

var str = 'Apples are round, and apples are juicy apples apples';
var newstr = str.replace('apples', 'oranges', 'gi');
console.log(newstr);

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
		}
	};

if ("skills" in bio) {
	console.log("skills in bio");
} else {
	console.log("skills");
}

if ("s" in bio) {
	console.log("s");
} else {
	console.log("ss");
}

for (w in bio.work) {
	console.log(w + " : " + bio.work[w]);
}

var work = {
	"jobs" : [
			{
				"employer" : "Udacity",
				"title" : "Course Developer",
				"location" : "Mountain View, CA",
				"dates" : "Feb 2014 - Current",
				"description" : "Who moved my cheese cheesy feet cauliflower cheese. Queso taleggio when the cheese comes out everybody's happy airedale ricotta cheese and wine paneer camembert de normandie. Swiss mozzarella cheese slices feta fromage frais airedale swiss cheesecake. Hard cheese blue castello halloumi parmesan say cheese stinking bishop jarlsberg."
			},
			{
				"employer" : "LearnBIG",
				"title" : "Software Engineer",
				"location" : "Seattle, WA",
				"dates" : "May 2013 - Jan 2014",
				"description" : "Who moved my cheese cheesy feet cauliflower cheese. Queso taleggio when the cheese comes out everybody's happy airedale ricotta cheese and wine paneer camembert de normandie. Swiss mozzarella cheese slices feta fromage frais airedale swiss cheesecake. Hard cheese blue castello halloumi parmesan say cheese stinking bishop jarlsberg."
			},
			{
				"employer" : "LEAD Academy Charter High School",
				"title" : "Science Teacher",
				"location" : "Nashville, TN",
				"dates" : "Jul 2012 - May 2013",
				"description" : "Who moved my cheese cheesy feet cauliflower cheese. Queso taleggio when the cheese comes out everybody's happy airedale ricotta cheese and wine paneer camembert de normandie. Swiss mozzarella cheese slices feta fromage frais airedale swiss cheesecake. Hard cheese blue castello halloumi parmesan say cheese stinking bishop jarlsberg."
			},
			{
				"employer" : "Stratford High School",
				"title" : "Science Teacher",
				"location" : "Nashville, TN",
				"dates" : "Jun 2009 - Jun 2012",
				"description" : "Who moved my cheese cheesy feet cauliflower cheese. Queso taleggio when the cheese comes out everybody's happy airedale ricotta cheese and wine paneer camembert de normandie. Swiss mozzarella cheese slices feta fromage frais airedale swiss cheesecake. Hard cheese blue castello halloumi parmesan say cheese stinking bishop jarlsberg."
			} ]
};

// Your code goes here! Let me help you get started

function locationizer(work) {
	var locs = [];
	for (var loc in work.jobs) {
		locs.push(work.jobs[loc].location);
	}
	return locs;
}

// Did locationizer() work? This line will tell you!
console.log(locationizer(work));

var inName = function(name) {
	var names = name.trim().split(" ");
	return names[0][0].toUpperCase() + names[0].slice(1).toLowerCase() + " "
			+ names[1].toUpperCase();
};

console.log(inName("je last"));

example();
function example() {
	console.log("Ran the example");
};

//anotherExample();
//var anotherExample = function() {
//	console.log("Ran the example");
//};