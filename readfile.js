/*
 *
 */
var fs = require("fs");

fs.readFile('comments.json', function(err, data) {
	if(err) {
		console.error(err);
		return;
	} else {
		console.log(data.toString());
	}
});

console.log("Program Ended");
