/*
 *
 */
var dataset = [5, 10, 13, 19, 21, 25, 22, 18, 15, 13,
	11, 12, 15, 20, 18, 17, 16, 18, 23, 25
];
var width = 500;
var height = 200;
var barPadding = 1;

var tip = d3.tip()
	.style({ "background": "rgba(0, 200, 0, 0.8)", "padding": "12px", "box-sizing": "border-box" })
	.offset([-10, 0])
	.html(function(d) {
		return "<strong>Pointing at: </strong><span style='color:red'>" + d + "</span>";
	});

var svg = d3.select("body").append("svg")
	.attr("width", width)
	.attr("height", height).call(tip);

svg.selectAll("rect").data(dataset).enter().append("rect")
	.attr("x", function(d, i) {
		return i * (width / dataset.length);
	})
	.attr("y", function(d) {
		return height - (d * 4);
	})
	.attr("width", width / dataset.length - barPadding)
	.attr("height", function(d) {
		return d * 4;
	})
	.attr("fill", function(d) {
		return "rgb(0, 0, " + (d * 10) + ")"
	})
	.on("mouseover", tip.show).on("mouseout", tip.hide);

svg.selectAll("text").data(dataset).enter().append("text")
	.text(function(d) {
		return d;
	})
	.attr("x", function(d, i) {
		return i * (width / dataset.length) + 5;
	})
	.attr("y", function(d) {
		return height - (d * 4) + 14;
	})
	.attr("font-family", "sans-serif")
	.attr("font-size", "11px")
	.attr("fill", "white");
