/*
 * D3 circles
 */

var jsonCirlces = [{
  "xaxis": 30,
  "yaxis": 30,
  "radius": 20,
  "color": "green"
}, {
  "xaxis": 70,
  "yaxis": 70,
  "radius": 20,
  "color": "purple"
}, {
  "xaxis": 100,
  "yaxis": 100,
  "radius": 20,
  "color": "red"
}];

var svgContainer = d3.select("body")
  .append("svg")
  .attr("width", 200)
  .attr("height", 200);

var circles = svgContainer.selectAll("circles")
  .data(jsonCirlces)
  .enter()
  .append("circle");

var circleAttributes = circles.attr("cx", function(d) {
    return d.xaxis;
  })
  .attr("cy", function(d) {
    return d.yaxis;
  })
  .attr("r", function(d) {
    return d.radius;
  })
  .style("fill", function(d) {
    return d.color;
  });
