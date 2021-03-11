var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(60, 1, 1,10000);
var access_token = window.localStorage.getItem("access_token");
camera.position.set(-1300, 540, 780);
scene.add(camera);

if (!window.WebGLRenderingContext) {
	alert ("This tool requires WebGL support to run!\nPlease use a newer browser with WebGL (recommended: Chrome or FireFox).");
}

var container = $("#canvas-container");
var renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, preserveDrawingBuffer: true });
container.append(renderer.domElement);

$(document).ready(onResize);
$(window).resize(onResize);
function onResize()
{
	renderer.setSize(container.width(), container.height());
}

var controls = new THREE.OrbitControls( camera, renderer.domElement );
controls.enableDamping = true;
controls.dampingFactor = 0.25;
controls.enableZoom = true;

var ambient_light = new THREE.AmbientLight( 0xE5E5E5 );
scene.add( ambient_light );

var box_mesh;

var resources = [];

var matrials = [];
				
function getTexture(type)
{	
	const _canvDom = $("#canvas-"+type)[0];
	//console.log($("#canvas-"+type) );
    const outsideCanv = new THREE.CanvasTexture(_canvDom);
	outsideCanv.minFilter = THREE.LinearFilter;
    outsideCanv.wrapS = THREE.ClampToEdgeWrapping;
    outsideCanv.wrapT = THREE.ClampToEdgeWrapping;
	resources.push(outsideCanv);
	return outsideCanv;
}

function getMaterial(type)
{
	const outsideMat = new THREE.MeshStandardMaterial({
		map: getTexture(type),
		side: THREE.DoubleSide,
	});
	outsideMat.skinning = true;
	resources.push(outsideMat);
	return outsideMat;
}


function renderProductBox()
{
	var w = parseInt($("#size-x").val());
	
	var h = parseInt($("#size-y").val());
	
	var d = parseInt($("#size-z").val());
	if (box_mesh) {clearProductBox();}
	var geometry = new THREE.BoxGeometry(w, h, d, 10, 10, 10);
	//var materialTransparent =  new THREE.MeshBasicMaterial( { transparent: true, opacity: 0, wireframe: true, side: THREE.DoubleSide} );
	resources.push(geometry);
	materials = [
		getMaterial("right"),
		getMaterial("left"),
		getMaterial("top"),
		getMaterial("bottom"),
		getMaterial("front"),
		getMaterial("back")
	];
	box_mesh = new THREE.Mesh(geometry, materials);
	resources.push(box_mesh);
	scene.add(box_mesh);
	
	for (side of sides)
		changeCanvasSize(side);
	

}

function renderProductBoxcheckout(w,h,d,materials){
	if (box_mesh) {clearProductBox();}
	var geometry = new THREE.BoxGeometry(w, h, d, 10, 10, 10);
	resources.push(geometry);	
	box_mesh = new THREE.Mesh(geometry, materials);
	resources.push(box_mesh);
	scene.add(box_mesh);
}


function saveModelToDatabase(){
	camera.rotation.set(-0.6055446444344589, -0.8117261390954865, -0.46544821952100746);
	camera.position.set(-1300,540,780);
	controls.update();
	render();
	var canvas = renderer.domElement;
	const imgData = canvas.toBlob( ( blob ) => {
		var form = new FormData();
		var w = parseInt($("#size-x").val());
		var h = parseInt($("#size-y").val());
		var d = parseInt($("#size-z").val());
		var name = $("#name").val();
		var access_token = window.localStorage.getItem("access_token");
		form.append("preview_image", blob,"preview.png");
		if(name)
			form.append("name", name);
		form.append("width", w);
		form.append("height", h);
		form.append("depth", d);
		form.append("front_texture",JSON.stringify(canvases['front'].toJSON()));
		form.append("top_texture", JSON.stringify(canvases['top'].toJSON()));
		form.append("bottom_texture", JSON.stringify(canvases['bottom'].toJSON()));
		form.append("back_texture", JSON.stringify(canvases['back'].toJSON()));
		form.append("right_texture", JSON.stringify(canvases['right'].toJSON()));
		form.append("left_texture", JSON.stringify(canvases['left'].toJSON()));
		form.append("material", material);

		$.ajax({
			"url": "/app/boxcreate/",
			"method": "POST",
			"timeout": 0,
			"headers": {
				"Authorization": access_token,
			},
			"processData": false,
			"mimeType": "multipart/form-data",
			"contentType": false,
			"data": form,
			success: function(response) {
				alert("Saved successfully!!!");
				window.location.pathname = '/app/saveddesign/';
			},
			error: function(xhr, a, b)
			{
				console.log(xhr);
			}
		});
	});
	
}

function checkoutTOSave(){
	camera.rotation.set(-0.6055446444344589, -0.8117261390954865, -0.46544821952100746);
	camera.position.set(-1300,540,780);
	controls.update();
	render();
	var canvas = renderer.domElement;
	const imgData = canvas.toBlob( ( blob ) => {
		var form = new FormData();
		var w = parseInt($("#size-x").val());
		var h = parseInt($("#size-y").val());
		var d = parseInt($("#size-z").val());
		var name = $("#name").val();
		var access_token = window.localStorage.getItem("access_token");
		form.append("preview_image", blob,"preview.png");
		if(name)
			form.append("name", name);
		form.append("width", w);
		form.append("height", h);
		form.append("depth", d);
		form.append("front_texture",JSON.stringify(canvases['front'].toJSON()));
		form.append("top_texture", JSON.stringify(canvases['top'].toJSON()));
		form.append("bottom_texture", JSON.stringify(canvases['bottom'].toJSON()));
		form.append("back_texture", JSON.stringify(canvases['back'].toJSON()));
		form.append("right_texture", JSON.stringify(canvases['right'].toJSON()));
		form.append("left_texture", JSON.stringify(canvases['left'].toJSON()));
		form.append("material", material);

		$.ajax({
			"url": "/app/boxcreate/",
			"method": "POST",
			"timeout": 0,
			"headers": {
				"Authorization": access_token,
			},
			"processData": false,
			"mimeType": "multipart/form-data",
			"contentType": false,
			"data": form,
			success: function(response) {
				var str = $("#unit_price").html().split(" ");
				response = JSON.parse(response)
				var box_id = response.id;
				$.ajax({
					"url":"/app/purchase/",
					"method":"POST",
					"headers": {
						"Authorization": access_token,
					},
					"data":{
						"box":box_id,
						"quantity":parseInt($("#quantity").val()),
						"unit_price":parseFloat(str[0])
					},
					success: function(response){
						window.location.pathname = '/app/checkout/'+response['id'];
					},
					error: function(xhr, a, b)
					{
						console.log(xhr);
					}
				})
			},
			error: function(xhr, a, b)
			{
				console.log(xhr);
			}
		});
	});
}

function checkoutTOEdit(){
	camera.rotation.set(-0.6055446444344589, -0.8117261390954865, -0.46544821952100746);
	camera.position.set(-1000,540,780);
	controls.update();
	render();
	var canvas = renderer.domElement;

	const imgData = canvas.toBlob( ( blob ) => {
		var form = new FormData();
		var w = parseInt($("#size-x").val());
		var h = parseInt($("#size-y").val());
		var d = parseInt($("#size-z").val());
		var name = $("#name").val();
		var access_token = window.localStorage.getItem("access_token");
		form.append("preview_image", blob,"preview.png");
		form.append("uuid",get_uuid());
		if(name)
			form.append("name", name);
		form.append("width", w);
		form.append("height", h);
		form.append("depth", d);
		form.append("front_texture",JSON.stringify(canvases['front'].toJSON()));
		form.append("top_texture", JSON.stringify(canvases['top'].toJSON()));
		form.append("bottom_texture", JSON.stringify(canvases['bottom'].toJSON()));
		form.append("back_texture", JSON.stringify(canvases['back'].toJSON()));
		form.append("right_texture", JSON.stringify(canvases['right'].toJSON()));
		form.append("left_texture", JSON.stringify(canvases['left'].toJSON()));
		form.append("material", material);
		$.ajax({
			"url": "/app/editbox/",
			"method": "PUT",
			"timeout": 0,
			"headers": {
				"Authorization": access_token,
			},
			"processData": false,
			"mimeType": "multipart/form-data",
			"contentType": false,
			"data": form,
			success: function(response) {
				var str = $("#unit_price").html().split(" ");
				response = JSON.parse(response)
				var box_id = response.id;
				$.ajax({
					"url":"/app/purchase/",
					"method":"POST",
					"headers": {
						"Authorization": access_token,
					},
					"data":{
						"box":box_id,
						"quantity":parseInt($("#quantity").val()),
						"unit_price":parseFloat(str[0])
					},
					success: function(response){
						window.location.pathname = '/app/checkout/'+response['id'];
					},
					error: function(xhr, a, b)
					{
						console.log(xhr);
					}
				})	
			},
			error: function(xhr, a, b)
			{
				console.log(xhr);
			}
		});
	});
}

function editModelToDatabase(){
	
	camera.rotation.set(-0.6055446444344589, -0.8117261390954865, -0.46544821952100746);
	camera.position.set(-1000,540,780);
	controls.update();
	render();
	var canvas = renderer.domElement;

	const imgData = canvas.toBlob( ( blob ) => {
		var form = new FormData();
		var w = parseInt($("#size-x").val());
		var h = parseInt($("#size-y").val());
		var d = parseInt($("#size-z").val());
		var name = $("#name").val();
		var access_token = window.localStorage.getItem("access_token");
		form.append("preview_image", blob,"preview.png");
		form.append("uuid",get_uuid());
		if(name)
			form.append("name", name);
		form.append("width", w);
		form.append("height", h);
		form.append("depth", d);
		form.append("front_texture",JSON.stringify(canvases['front'].toJSON()));
		form.append("top_texture", JSON.stringify(canvases['top'].toJSON()));
		form.append("bottom_texture", JSON.stringify(canvases['bottom'].toJSON()));
		form.append("back_texture", JSON.stringify(canvases['back'].toJSON()));
		form.append("right_texture", JSON.stringify(canvases['right'].toJSON()));
		form.append("left_texture", JSON.stringify(canvases['left'].toJSON()));
		form.append("material", material);
		$.ajax({
			"url": "/app/editbox/",
			"method": "PUT",
			"timeout": 0,
			"headers": {
				"Authorization": access_token,
			},
			"processData": false,
			"mimeType": "multipart/form-data",
			"contentType": false,
			"data": form,
			success: function(response) {
				alert("Updated Successfully !!!");
				window.location.pathname = '/app/saveddesign/';
			},
			error: function(xhr, a, b)
			{
				console.log(xhr);
			}
		});
	});
}

function tryRenderProduct()
{
	try
	{
		renderProductBox();
	}
	catch (e)
	{
		setTimeout(tryRenderProduct, 100);
	}
}
tryRenderProduct();

function clearProductBox()
{
	
	scene.remove(box_mesh);
	for (var i = 0; i < resources.length; ++i)
	{
		var curr = resources[i];
		if (curr.dispose) {curr.dispose();}
	}
	resources = [];	
}

requestAnimationFrame = requestAnimationFrame || function(callback) {setTimeout(callback, 1000/60);};

function render() {
	requestAnimationFrame(render);
	renderer.render(scene, camera);
}
render();