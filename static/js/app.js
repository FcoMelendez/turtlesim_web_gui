var turtle = new Image();
var turtleData = {"x":0.0, "y":0.0, "theta":0.0};
var canvas = {};
var ctx = {}

function getMousePos(my_canvas, evt) {
  var rect = my_canvas.getBoundingClientRect();
  return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top
  };
}

function init() {
  turtle.src = '/static/images/turtle.png';
  canvas = document.getElementById('canvas');
  canvas.width = 600;
  canvas.height = 600;
  ctx = document.getElementById('canvas').getContext('2d');
  setInterval(readTurtleData, 200);
  window.requestAnimationFrame(draw);
  canvas.addEventListener('mousemove', function(evt) {
        var mousePos = getMousePos(canvas, evt);
        var message = 'Mouse position: ' + mousePos.x + ',' + mousePos.y;
        console.log(message);
      }, false);
}

function readTurtleData(){
  var settings = {
    "url": "/turtleValues",
    "method": "GET"
  };

  $.ajax(settings).done(function (response) {
    turtleData = JSON.parse(response); 
  });
}

function draw() { 
  ctx.globalCompositeOperation = 'destination-over';
  ctx.clearRect(0, 0, 600, 600); // clear canvas
  ctx.fillStyle = 'rgba(0, 0, 150, 0.4)';
  ctx.fillRect(50, 50, canvas.width-100, canvas.height-100);

  // Moon
  ctx.save();
  //ctx.translate(0, 28.5);
  var x_pose = 50-22+parseFloat(turtleData.x).toFixed(2)*500/11;
  var y_pose = 50-22+500-parseFloat(turtleData.y).toFixed(2)*500/11;
  ctx.translate(x_pose+22, y_pose+22);
  var theta_pose = parseFloat(turtleData.theta-Math.PI/2).toFixed(2);
  ctx.rotate(-theta_pose);
  ctx.drawImage(turtle, -22, -22);
  ctx.rotate(theta_pose);
  ctx.translate(+x_pose-22, -y_pose-22);
  ctx.restore();
  ctx.beginPath();
  ctx.arc(150, 150, 105, 0, Math.PI * 2, false); // Earth orbit
  ctx.stroke();

  window.requestAnimationFrame(draw);
}
