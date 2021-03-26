var material = "kraft";
var decoration = false;
var background_color = false;
var canvases={};
var object_cnt = 0;
var sides = ['front','back','left','right','bottom','top'];
var face = {
  'front':[672, 519, 1281],
  'back':[-679, 644, -1220],
  'left':[-1323, 615, 703],
  'right':[1293, 583, -592],
  'bottom':[-54, -1532, 125],
  'top':[-250, 1498, 241],
}
function selectCurrentObject(value){
  canvases[value].setActiveObject(canvases[value].item(object_cnt));
  object_cnt++;
}
function updatePrice(w,h,d,q){
  var access_token = window.localStorage.getItem("access_token");
  $.ajax({
    url: "/app/getmaterailprice/",
    type: "POST",
    "headers": {
      "Authorization": access_token,
    },
    data:{
      "csrfmiddlewaretoken" : "{{ csrf_token }}",
      "material":material
    },
    success: function(response) {
      let base_price = response['material_price'];
      let price = calculatingPrice(base_price,w,h,d);
      price = Math.round(price*100)/100;
      $("#unit_price").html(price + " INR");
      price = Math.round(q*price*100)/100;
      $("#subtotal").html(price + " INR");       
    },
    error: function(xhr, a, b){
      console.log(xhr);
    }
  });
}

$("#quantity").change(function(){
  let w = parseInt($("#size-x").val());
	let h = parseInt($("#size-y").val());
	let d = parseInt($("#size-z").val());
  let q = parseInt($("#quantity").val());
  if(q>2000)
    $("#message_quantity").html("For quantity greater than 2000 please contact us directly")
  else{
    $("#message_quantity").html("")
    updatePrice(w,h,d,q)
  }
});

function setQuantity(q){
  $("#quantity").val(q);
  let w = parseInt($("#size-x").val());
	let h = parseInt($("#size-y").val());
	let d = parseInt($("#size-z").val());
  updatePrice(w,h,d,q);
}

$("#update_size").click(function(){
  let w = parseInt($("#size-x").val());
	let h = parseInt($("#size-y").val());
	let d = parseInt($("#size-z").val());
  let q = parseInt($("#quantity").val());
  if(w>=400 && w<=900 && h>=400 && h<=900 && d>=400 && d<=900){
    renderProductBox();
    $("#message").html("");
    updatePrice(w,h,d,q);
  }
  else
    $("#message").html("width, height and depth should be between 400 and 900");
});

document.getElementById('background-color').onchange = function() {
  let value =  (document.getElementById("textures").value).toLowerCase(); 
  canvases[value].backgroundImage = 0;
  canvases[value].backgroundColor= this.value ;
  canvases[value].renderAll();
};

document.getElementById('background-color').onclick = function() {
  let value =  (document.getElementById("textures").value).toLowerCase(); 
  canvases[value].backgroundImage = 0;
  canvases[value].backgroundColor= this.value ;
  canvases[value].renderAll();
};

document.getElementById('fit').onclick = function(){
  let value =  (document.getElementById("textures").value).toLowerCase(); 
  let h = canvases[value].height;
  let w = canvases[value].width;
  (canvases[value].getActiveObject()).scaleToHeight(h);
  (canvases[value].getActiveObject()).scaleToWidth(w);
  (canvases[value].getActiveObject()).center();
  canvases[value].renderAll();
};

document.getElementById('center').onclick = function(){
  let value =  (document.getElementById("textures").value).toLowerCase(); 
  (canvases[value].getActiveObject()).center();
  canvases[value].renderAll();
};

document.getElementById('fit_text').onclick = function(){
  let value =  (document.getElementById("textures").value).toLowerCase(); 
  let h = canvases[value].height;
  let w = canvases[value].width;
  (canvases[value].getActiveObject()).scaleToHeight(h);
  (canvases[value].getActiveObject()).scaleToWidth(w);
  (canvases[value].getActiveObject()).center();
  canvases[value].renderAll();
};

document.getElementById('center_text').onclick = function(){
  let value =  (document.getElementById("textures").value).toLowerCase(); 
  (canvases[value].getActiveObject()).center();
  canvases[value].renderAll();
};

document.getElementById('reset-background').onclick = function() {
  let value =  (document.getElementById("textures").value).toLowerCase(); 
  canvases[value].backgroundColor= 0;
  setBackgroundCanvas(value,material);
};

function Addtext() {
  var value =  ($("#textures").val()).toLowerCase();
  var object = {
    left: 10,
    top: 10,
    fontFamily: 'helvetica neue',
    fill: '#000',
    stroke: '#fff',
    strokeWidth: .1,
    fontSize: 25
  }
  canvases[value].add(new fabric.IText('Tap and Type', object));
  selectCurrentObject(value);

}
      
document.getElementById('text-color').onchange = function() {
  let value =  (document.getElementById("textures").value).toLowerCase(); 
  canvases[value].getActiveObject().setColor(this.value);
  canvases[value].renderAll();
};

document.getElementById('text-bg-color').onchange = function() {
  let value =  (document.getElementById("textures").value).toLowerCase();
  canvases[value].getActiveObject().set('backgroundColor',this.value);
  canvases[value].renderAll();
};
      
document.getElementById('text-stroke-color').onchange = function() {
  let value =  (document.getElementById("textures").value).toLowerCase();
  canvases[value].getActiveObject().set('stroke',this.value);
  canvases[value].renderAll();
};

document.getElementById('text-stroke-width').onchange = function() {
  let value =  (document.getElementById("textures").value).toLowerCase();
  canvases[value].getActiveObject().set('strokeWidth',this.value);
  canvases[value].renderAll();
};

document.getElementById('font-family').onchange = function() {
  let value =  (document.getElementById("textures").value).toLowerCase();
  canvases[value].getActiveObject().set('fontFamily',this.value);
  canvases[value].renderAll();
};

document.getElementById('text-font-size').onchange = function() {
  let value =  (document.getElementById("textures").value).toLowerCase();
  if(this.value > 40)
    $("#text_message").html("Font size should be less than or equal to 40")
  else{
    $("#text_message").html("");
    canvases[value].getActiveObject().set('fontSize',this.value);
    canvases[value].renderAll();
  }
};
      
//document.getElementById('text-align').onchange = function() {
//let value =  (document.getElementById("textures").value).toLowerCase(); 
  //canvases[value].getActiveObject().set('textAlign',this.value);
  //canvases[value].renderAll();
//};      
radios5 = document.getElementsByName("fonttype"); 
for (var i = 0, max = radios5.length; i < max; i++) {
  radios5[i].onclick = function() {
    let value =  (document.getElementById("textures").value).toLowerCase(); 
    if (document.getElementById(this.id).checked == true) {
      if (this.id == "text-cmd-bold") {
        canvases[value].getActiveObject().set("fontWeight", "bold");
      }
      if (this.id == "text-cmd-italic") {
        canvases[value].getActiveObject().set("fontStyle", "italic");
      }
      if (this.id == "text-cmd-underline") {
        canvases[value].getActiveObject().set("underline", true );
      }
      if (this.id == "text-cmd-linethrough") {
        canvases[value].getActiveObject().set("linethrough",true);
      }
      if (this.id == "text-cmd-overline") {
        canvases[value].getActiveObject().set("overline",true);
      }
    } 
    else {
      if (this.id == "text-cmd-bold") {
        canvases[value].getActiveObject().set("fontWeight", "");
      }
      if (this.id == "text-cmd-italic") {
        canvases[value].getActiveObject().set("fontStyle", "");
      }
      if (this.id == "text-cmd-underline") {
        canvases[value].getActiveObject().set("underline", false);
      }
      if (this.id == "text-cmd-linethrough") {
        canvases[value].getActiveObject().set("linethrough", false);
      }
      if (this.id == "text-cmd-overline") {
        canvases[value].getActiveObject().set("overline", false);
      }
    }
    canvases[value].renderAll();
  }
}
      
function readURL(input,side) {
  if (input.files && input.files[0]) {
    var size  = input.files[0].size;
    var max_size = 256000;
    if(size>max_size){
      $("#file_message").html("file size exceeds 250KB");
    }
    else{
      $("#file_message").html("");
      var reader = new FileReader();
      reader.onload = function (e) {
        canvas = canvases[side];
        fabric.Image.fromURL(e.target.result, function(img) {
          var oImg = img.set({
                      left: 0,
                      top: 0,
                      angle: 0,
                    }).scale(0.2);
          canvas.add(oImg).renderAll();
          selectCurrentObject(side);
        });
      };
      reader.readAsDataURL(input.files[0]);
    }
  }
}

function changeSize(x,y,z){
  $("#size-x").val(x);
  $("#size-y").val(y);
  $("#size-z").val(z);
  renderProductBox();
}

function setCamera(x, y, z){
	camera.rotation.set(-0.6055446444344589, -0.8117261390954865, -0.46544821952100746);
	camera.position.set(x,y,z);
	controls.update();
}

function changeCanvasSize(side){
  if(side=='left' || side=='right'){
    $("#canvas-"+side).css('height',$("#size-y").val()/3);
    $("#canvas-"+side).css('width',$("#size-z").val()/3);
    canvases[side].setHeight($("#size-y").val()/3);
    canvases[side].setWidth($("#size-z").val()/3);
  }

  else if(side=='front' || side=='back'){
    $("#canvas-"+side).css('height',$("#size-y").val()/3);
    $("#canvas-"+side).css('width',$("#size-x").val()/3);
    canvases[side].setHeight($("#size-y").val()/3);
    canvases[side].setWidth($("#size-x").val()/3);
  }

  else{
    $("#canvas-"+side).css('height',$("#size-x").val()/3);
    $("#canvas-"+side).css('width',$("#size-z").val()/3);
    canvases[side].setHeight($("#size-x").val()/3);
    canvases[side].setWidth($("#size-z").val()/3);
  }
  if(canvases[side].backgroundImage!=null){
    setBackgroundCanvas(side,material);
  }
  canvases[side].renderAll();
}
      
function changeBoxTexture(texture){
  for(side of sides){
    canvases[side]=setBackgroundCanvas(side,texture);
  }
}

$("#textures").change(function(){
  var value =  ($("#textures").val()).toLowerCase(); 
  for(side of sides){
    if(side == value){
      changeCanvasSize(side);
      $("#"+side).css('display','block');
      $("#c-"+side).css('display','block');
      setCamera(face[side][0], face[side][1], face[side][2]);
    }
    else{
      $("#"+side).css('display','none');
      $("#c-"+side).css('display','none');
    } 
  } 
});

function setBackgroundCanvas(side,image){
  var canvas;
  material = image;
  let w = parseInt($("#size-x").val());
	let h = parseInt($("#size-y").val());
	let d = parseInt($("#size-z").val());
  let q = parseInt($("#quantity").val());
  updatePrice(w,h,d,q);
  if(!canvases[side])
    canvas = new fabric.Canvas("canvas-"+side);
  else  
    canvas = canvases[side];
 
    if(material=='kraft'){ 
      fabric.Image.fromURL("http://127.0.0.1:8000/static/images/kraft.jpg", function(img) {
        canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas), {
          scaleX: canvas.width / img.width,
          scaleY: canvas.height / img.height
        });
      });
    }
    else if(material=='white'){
      fabric.Image.fromURL("http://127.0.0.1:8000/static/images/white.jpg", function(img) {
        canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas), {
          scaleX: canvas.width / img.width,
          scaleY: canvas.height / img.height
        });
      });
    }
    else if(material == 'dreamcoat'){
      fabric.Image.fromURL("http://127.0.0.1:8000/static/images/gray.jpg", function(img) {
        canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas), {
          scaleX: canvas.width / img.width,
          scaleY: canvas.height / img.height
        });
      });
    }

    canvas.on("after:render", function () {
      if (box_mesh) {
        for (const material of box_mesh.material) {
          if (material.map) {
            material.map.needsUpdate = true;
          }
        }
      }
    });
  
	return canvas;
}
      
window.deleteObject = function() {
  var value =  ($("#textures").val()).toLowerCase(); 
  var canvas = canvases[value]
  canvas.remove(canvas.getActiveObject());
  canvas.renderAll(); 
}

function calculateSurfaceArea(length,width,height){
  let surface_area = 2*((length*width)+(width*height)+(length*height))
  return surface_area;
}

function calculatingPrice(base_price,length,width,height){
  let surface_area = calculateSurfaceArea(length,width,height);
  let base_area =  calculateSurfaceArea(360,360,360);
  let price = (surface_area * base_price)/base_area;
  return price;
}

if(window.location.pathname=='/app/boxdesign/'){
  for(side of sides){
    canvases[side]=setBackgroundCanvas(side,"kraft");
  }
  renderProductBox();
  $("#save").click(function(e){saveModelToDatabase();});
  updatePrice(500,500,500,250);
  $("#checkout").click(function(e){checkoutTOSave();});
}
else{
  function get_uuid(){
    uuid = window.location.pathname;
    uuid = uuid.split("/")[3];
    return uuid;
  }
  $("#edit_box").html("<a href='/app/editbox/"+get_uuid()+"/'>Edit</a>");
  var box;
  var access_token = window.localStorage.getItem("access_token");
  $.ajax({
    url: "/app/getbox/",
    type: "POST",
    "headers": {
      "Authorization": access_token,
    },
    data:{
      "csrfmiddlewaretoken" : "{{ csrf_token }}",
      "uuid":get_uuid()
    },
    async: false,
    success: function(response) {
      box = response;              
    },
    error: function(xhr, a, b){
      console.log(xhr);
    }
  });

  for(side of sides){
    canvases[side]=new fabric.Canvas("canvas-"+side);
    canvases[side].loadFromJSON(box[side+"_texture"], canvases[side].renderAll.bind(canvases[side]), function(o, object) {});
    canvases[side].on("after:render", function () {
      if (box_mesh) {
        for (const material of box_mesh.material) {
          if (material.map) {
            material.map.needsUpdate = true;
          }
        }
      }
    });
  }

  material = box.material;
  $("#size-x").val(box.width);
	$("#size-y").val(box.height);
  $("#size-z").val(box.depth);
  $("#name").val(box.name);
  let w = box.width
	let h = box.height
	let d = box.depth
  let q = 250
  updatePrice(w,h,d,q);
  renderProductBox();
  $("#save").click(function(e){editModelToDatabase();});
  $("#checkout").click(function(e){checkoutTOEdit();});
} 