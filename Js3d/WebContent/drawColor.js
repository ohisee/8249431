/*
 * 
 */

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
/*global THREE, requestAnimationFrame, Detector, Stats, dat window document Coordinates*/
var camera, scene, renderer;
var cameraControls;
var clock = new THREE.Clock();
var ambientLight, light;

function init() {
	var canvasWidth = 846;
	var canvasHeight = 494;
	var canvasRatio = canvasWidth / canvasHeight;

	// CAMERA

	camera = new THREE.PerspectiveCamera( 45, canvasRatio, 1, 80000 );
	camera.position.set( -300, 300, -1000 );
	camera.lookAt(0,0,0);
	// LIGHTS

	ambientLight = new THREE.AmbientLight( 0xffffff );

	light = new THREE.DirectionalLight( 0xffffff, 0.7 );
	light.position.set( -800, 900, 300 );

	// RENDERER
	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setSize( canvasWidth, canvasHeight );
	renderer.setClearColorHex( 0xAAAAAA, 1.0 );

	renderer.gammaInput = true;
	renderer.gammaOutput = true;

	// CONTROLS
	cameraControls = new THREE.OrbitAndPanControls( camera, renderer.domElement );
	cameraControls.target.set(0, 0, 0);

	fillScene();
	// GUI
}

function createBall() {
    // Do not change the color itself, change the material and use the ambient and diffuse components". 
	//var material = new THREE.MeshBasicMaterial( { color: 0xFF0000, shading: THREE.FlatShading } );
	//var material = new THREE.MeshLambertMaterial({ color: 0xFF0000, shading: THREE.FlatShading } );
	var material = new THREE.MeshLambertMaterial({ color: 0xFF0000 } );
	var newAmbientR = material.color.r * 0.4;
	var newAmbientG = material.color.g * 0.4;
	var newAmbientB = material.color.b * 0.4;
	material.ambient.setRGB(newAmbientR, newAmbientG, newAmbientB);
	
	var sphere = new THREE.Mesh( new THREE.SphereGeometry( 400, 64, 32 ), material );
	return sphere;
}

function fillScene() {
	scene = new THREE.Scene();
	scene.fog = new THREE.Fog( 0x808080, 2000, 4000 );
	scene.add( camera );

	// LIGHTS
	scene.add( ambientLight );
	scene.add( light );

	var ball = createBall();
	scene.add( ball );

	//Coordinates.drawGround({size:1000});
	//Coordinates.drawGrid({size:1000,scale:0.01});
	//Coordinates.drawAllAxes({axisLength:500,axisRadius:1,axisTess:4});
}

function addToDOM() {
    var container = document.getElementById('container');
    var canvas = container.getElementsByTagName('canvas');
    if (canvas.length>0) {
        container.removeChild(canvas[0]);
    }
    container.appendChild( renderer.domElement );
}

function animate() {

	window.requestAnimationFrame( animate );
	render();
	
}

function render() {
	var delta = clock.getDelta();
	cameraControls.update(delta);
	
	renderer.render( scene, camera );

}

init();
addToDOM();
animate();