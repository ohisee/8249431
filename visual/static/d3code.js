/*
 * D3
 */
var theData = [1, 2, 3];

var p = d3.select("body")
  .selectAll("p")
  .data(theData)
  .enter()
  .append("p")
  .text(function (d) {return d;});
