/**
 * New node file
 */

var Car = function(loc) {
	this.loc = loc;
};
Car.prototype.move = function() {
	this.loc++;
};


/**
 * Van
 */
var Van = function (loc) {
	Car.call(this, loc);
};
Van.prototype = Object.create(Car.prototype);
Van.prototype.constructor = Van;
Van.prototype.grab = function () {};

var zed = new Car(3);
zed.move();

var amy = new Van(9);
amy.move();
//amy.grab();

console.log(amy.constructor);