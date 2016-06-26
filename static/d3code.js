/*
 * D3
 */
var width = 900;
var height = 200;
var svg = d3.select("#content").append("svg").attr("width", width).attr("height", height);
var y = d3.scale.linear().domain([15, 90]).range([150, 0]);
var x = d3.scale.log().domain([250, 100000]).range([0, 250]);
var xaxis = d3.svg.axis().scale(d3.scale.linear().domain([0, 100]).range([0, 250])).orient("bottom");
var yaxis = d3.svg.axis().scale(d3.scale.linear().domain([10, 0]).range([0, 150])).orient("left");

svg.append('circle')
	.attr('r', 10)
	.attr('fill', 'red')
	.attr('cx', x(8347))
	.attr('cy', y(75));

svg.append("g")
	.attr("transform", "translate(24, 155)")
	.attr("font-size", "10px")
	.call(xaxis);

svg.append("g")
	.attr("transform", "translate(30, 10)")
	.attr("font-size", "10px")
	.call(yaxis);

svg.append("text").text("operation")
	.attr("transform", "rotate(-90)")
	.attr("x", -90)
	.attr("y", 50)
	.attr("font-size", "20px")
	.attr("fill", "blue");
