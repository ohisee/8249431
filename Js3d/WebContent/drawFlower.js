////////////////////////////////////////////////////////////////////////////////
// Make a Flower
////////////////////////////////////////////////////////////////////////////////
/*global THREE, Coordinates, document, window, dat*/

var camera, scene, renderer;
var cameraControls, effectController;
var clock = new THREE.Clock();
var gridX = true;
var gridY = false;
var gridZ = false;
var axes = true;
var ground = true;


function fillScene() {
	scene = new THREE.Scene();
	scene.fog = new THREE.Fog( 0x808080, 2000, 4000 );

	// LIGHTS
	var ambientLight = new THREE.AmbientLight( 0x222222 );
	var light = new THREE.DirectionalLight( 0xffffff, 1.0 );
	light.position.set( 200, 400, 500 );
	var light2 = new THREE.DirectionalLight( 0xffffff, 1.0 );
	light2.position.set( -500, 250, -200 );
	scene.add(ambientLight);
	scene.add(light);
	scene.add(light2);

    // FLOWER
    var petalMaterial = new THREE.MeshLambertMaterial( { color: 0xCC5920 } );
	var flowerHeight = 200;
	var petalLength = 120;
	var cylGeom = new THREE.CylinderGeometry( 15, 0, petalLength, 32 );
	var flower = new THREE.Object3D();
    /////////
    // YOUR CODE HERE
	// add code here to make 24 petals, radiating around the sphere
	// Just rotates and positions on the cylinder and petals are needed.
	var cylinder = new THREE.Mesh( cylGeom, petalMaterial );
	var petal = new THREE.Object3D();
	petal.add( cylinder );

	flower.add( petal );
	
	var stamenMaterial = new THREE.MeshLambertMaterial( { color: 0x333310 } );
	var stamen = new THREE.Mesh( 
		new THREE.SphereGeometry( 20, 32, 16 ), stamenMaterial );
	stamen.position.y = flowerHeight;	// move to flower center
	flower.add( stamen );
	
	//var flowerPetal = new THREE.Object3D();
	for (var i=0; i < 24; i++) {
		var cylinder = new THREE.Mesh( cylGeom, petalMaterial );
		var radian = i * (360/24) * (Math.PI/180);
		//var angle = (Math.PI/2) + (i / 24) * 2 * Math.PI;
		//cylinder.position.y = (petalLength/2) * Math.cos( angle );
		//cylinder.position.x = (petalLength/2);
		//cylinder.position.z = (petalLength/2) * Math.sin( angle );
		//cylinder.rotation.z = (90) * (Math.PI/180);
		//cylinder.rotation.x = angle;
		cylinder.position.y = (petalLength/2);
		
		var flowerPetal = new THREE.Object3D();
		flowerPetal.add(cylinder);
		flowerPetal.rotation.z = (90) * (Math.PI/180);
		flowerPetal.rotation.y = radian;
		flowerPetal.position.y = flowerHeight;
		
		//petal.position.x = (petalLength/2) * Math.cos( angle );
		//petal.position.z = (petalLength/2) * Math.sin( angle );
		//petal.rotation.x = (90) * (Math.PI/180);
		//petal.rotation.z = 90 * (Math.PI/180);
		
		flower.add(flowerPetal);
		
	}
	//flowerPetal.position.y = flowerHeight;
	//flowerPetal.rotation.z = (90) * (Math.PI/180);
	//flower.add(flowerPetal);

	var stemMaterial = new THREE.MeshLambertMaterial( { color: 0x339424 } );
	var stem = new THREE.Mesh( 
		new THREE.CylinderGeometry( 10, 10, flowerHeight, 32 ), stemMaterial );
	stem.position.y = flowerHeight/2;	// move from ground to stamen
	flower.add( stem );

	scene.add( flower );

}


function init() {
	var canvasWidth = 846; 
	var canvasHeight = 494;
	var canvasRatio = canvasWidth / canvasHeight;

	// RENDERER
	renderer = new THREE.WebGLRenderer( { antialias: false } );
	renderer.gammaInput = true;
	renderer.gammaOutput = true;
	renderer.setSize(canvasWidth, canvasHeight);
	renderer.setClearColorHex( 0xAAAAAA, 1.0 );

	// CAMERA
	camera = new THREE.PerspectiveCamera( 38, canvasRatio, 1, 10000 );
	// CONTROLS
	cameraControls = new THREE.OrbitAndPanControls(camera, renderer.domElement);
	camera.position.set(-200, 400, 20);
	cameraControls.target.set(0,150,0);
	fillScene();

}

function addToDOM() {
    var container = document.getElementById('container');
    var canvas = container.getElementsByTagName('canvas');
    if (canvas.length>0) {
        container.removeChild(canvas[0]);
    }
    container.appendChild( renderer.domElement );
}

function drawHelpers() {
  if (ground) {
		Coordinates.drawGround({size:10000});		
	}
	if (gridX) {
		Coordinates.drawGrid({size:10000,scale:0.01});
	}
	if (gridY) {
		Coordinates.drawGrid({size:10000,scale:0.01, orientation:"y"});
	}
	if (gridZ) {
		Coordinates.drawGrid({size:10000,scale:0.01, orientation:"z"});	
	}
	if (axes) {
		Coordinates.drawAllAxes({axisLength:200,axisRadius:1,axisTess:50});
	}
}

function animate() {
	window.requestAnimationFrame(animate);
	render();
}

function render() {
	var delta = clock.getDelta();
	cameraControls.update(delta);

	if ( effectController.newGridX !== gridX || effectController.newGridY !== gridY || effectController.newGridZ !== gridZ || effectController.newGround !== ground || effectController.newAxes !== axes)
	{
		gridX = effectController.newGridX;
		gridY = effectController.newGridY;
		gridZ = effectController.newGridZ;
		ground = effectController.newGround;
		axes = effectController.newAxes;

		fillScene();
	}

	renderer.render(scene, camera);
}



function setupGui() {

	effectController = {

		newGridX: gridX,
		newGridY: gridY,
		newGridZ: gridZ,
		newGround: ground,
		newAxes: axes

	};

	var gui = new dat.GUI();
	var h = gui.addFolder("Grid display");
	h.add( effectController, "newGridX").name("Show XZ grid");
	h.add( effectController, "newGridY" ).name("Show YZ grid");
	h.add( effectController, "newGridZ" ).name("Show XY grid");
	h.add( effectController, "newGround" ).name("Show ground");
	h.add( effectController, "newAxes" ).name("Show axes");

}


// this is the main action sequence
init();
fillScene();
drawHelpers();
addToDOM();
setupGui();
animate();