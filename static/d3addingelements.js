/*
 *
 */
var dataset = [5, 10, 15, 20, 25];

var p = d3.select("body")
	.append("p")
	.text("New Paragragh!");

var p2 = d3.select("body")
	.data(dataset)
	.enter()
	.append("p")
	.text("New Paragragh");

var p3 = d3.select("body")
	.selectAll("p")
	.data(dataset)
	.enter().append("p").text(function(d) {
		return "New Paragragh " + d;
	}).style("color", "red");
