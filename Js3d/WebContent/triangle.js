/*
 * 
 */


// Define a triangle
var triangleGeometry = new THREE.Geometry();

// Vertices
triangleGeometry.vertices.push( new THREE.Vector3(1, 2, 0) ); // at index 0
triangleGeometry.vertices.push( new THREE.Vector3(3, 1, 0) ); // at index 1
triangleGeometry.vertices.push( new THREE.Vector3(3, 3, 0) ); // at index 2

// Face
triangleGeometry.faces.push(new THREE.Face3(0, 1, 2) );

// Make and position the vertical part of the step
stepMesh = new THREE.Mesh( stepVertical, stepMaterialVertical );
// The position is where the center of the block will be put.
// You can define position as THREE.Vector3(x, y, z) or in the following way:
stepMesh.position.x = 0;			// centered at origin
stepMesh.position.y = verticalStepHeight/2;	// half of height: put it above ground plane
stepMesh.position.z = 0;			// centered at origin
scene.add( stepMesh );

// Make and position the horizontal part
stepMesh = new THREE.Mesh( stepHorizontal, stepMaterialHorizontal );
stepMesh.position.x = 0;
// Push up by half of horizontal step's height, plus vertical step's height
stepMesh.position.y = stepThickness/2 + verticalStepHeight;
// Push step forward by half the depth, minus half the vertical step's thickness
stepMesh.position.z = horizontalStepDepth/2 - stepHalfThickness;
scene.add( stepMesh );

//
// second vertical
//
// Make and position the vertical part of the step
stepMesh = new THREE.Mesh( stepVertical, stepMaterialVertical );
// The position is where the center of the block will be put.
// You can define position as THREE.Vector3(x, y, z) or in the following way:
stepMesh.position.x = 0;			// centered at origin
// Push up by half of horizontal step's height, plus vertical step's height
stepMesh.position.y = verticalStepHeight/2 + stepThickness + verticalStepHeight;
// Push step forward by half the depth, minus half the vertical step's thickness
//stepMesh.position.z = (horizontalStepDepth/2 - stepHalfThickness) + (horizontalStepDepth/2 - stepHalfThickness);
stepMesh.position.z = horizontalStepDepth/2 - stepHalfThickness + horizontalStepDepth/2 - stepHalfThickness;
scene.add( stepMesh );

//
// second horizontal
//
// Make and position the horizontal part
stepMesh = new THREE.Mesh( stepHorizontal, stepMaterialHorizontal );
stepMesh.position.x = 0;
// Push up by half of horizontal step's height, plus vertical step's height
stepMesh.position.y = stepThickness/2 + verticalStepHeight + verticalStepHeight + stepThickness;
// Push step forward by half the depth, minus half the vertical step's thickness
//stepMesh.position.z = (horizontalStepDepth/2 - stepHalfThickness) + (horizontalStepDepth - stepThickness);
stepMesh.position.z = (horizontalStepDepth/2 - stepHalfThickness) * 3;
scene.add( stepMesh );


//
// third vertical
//
// Make and position the vertical part of the step
stepMesh = new THREE.Mesh( stepVertical, stepMaterialVertical );
// The position is where the center of the block will be put.
// You can define position as THREE.Vector3(x, y, z) or in the following way:
stepMesh.position.x = 0;			// centered at origin
// Push up by half of horizontal step's height, plus vertical step's height
stepMesh.position.y = verticalStepHeight/2 + stepThickness + verticalStepHeight + stepThickness + verticalStepHeight;
// Push step forward by half the depth, minus half the vertical step's thickness
//stepMesh.position.z = (horizontalStepDepth - stepThickness) + (horizontalStepDepth - stepThickness);
stepMesh.position.z = (horizontalStepDepth/2 - stepHalfThickness) * 4;
scene.add( stepMesh );

//
// third horizontal
//
// Make and position the horizontal part
stepMesh = new THREE.Mesh( stepHorizontal, stepMaterialHorizontal );
stepMesh.position.x = 0;
// Push up by half of horizontal step's height, plus vertical step's height
stepMesh.position.y = stepThickness/2 + verticalStepHeight + verticalStepHeight + stepThickness + verticalStepHeight + stepThickness;
// Push step forward by half the depth, minus half the vertical step's thickness
//stepMesh.position.z = (horizontalStepDepth/2 - stepHalfThickness)  + (horizontalStepDepth/2 - stepHalfThickness) + (horizontalStepDepth/2 - stepHalfThickness) + (horizontalStepDepth/2 - stepHalfThickness) + (horizontalStepDepth/2 - stepHalfThickness);
stepMesh.position.z = (horizontalStepDepth/2 - stepHalfThickness) * 5;
scene.add( stepMesh );


var nextStaircaseHeight = stepThickness + verticalStepHeight;
//var z = 0;
var yVerticalBase = verticalStepHeight/2;
var yHorizontalBased = stepThickness/2 + verticalStepHeight;
var zVerticalBase = horizontalStepDepth - stepThickness;
var zBase = horizontalStepDepth/2 - stepHalfThickness;
for (var steps = 0; steps < 6; steps++) {
	//Vertical
	stepMesh = new THREE.Mesh( stepVertical, stepMaterialVertical );
	stepMesh.position.x = 0;
	stepMesh.position.y = yVerticalBase + (nextStaircaseHeight * steps);
	stepMesh.position.z = zVerticalBase * steps;
	//verticalBase = verticalBase + stepThickness + verticalStepHeight;
	//yVerticalBase = yVerticalBase + nextStaircaseHeight;
	scene.add( stepMesh );
	//z = z + 1;
	
	//Horizontal
	stepMesh = new THREE.Mesh( stepHorizontal, stepMaterialHorizontal );
	stepMesh.position.x = 0;
	stepMesh.position.y = yHorizontalBased + (nextStaircaseHeight * steps);
	stepMesh.position.z = zBase + (zVerticalBase * steps);
	scene.add( stepMesh );
	//yHorizontalBased = yHorizontalBased + nextStaircaseHeight;
	scene.add( stepMesh );
	//z = z + 1;
}

