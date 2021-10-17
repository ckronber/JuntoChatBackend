//var submit = document.getElementById("submitMessage").value;
//var form = document.getElementById("listItem");
//var input = document.getElementById("noteMSG");


$(document).ready(function() {
  const socket = io();

  socket.on("disconnect", () => {
    console.log("user disconnected");
  });

  socket.on('connect', function() {
    socket.emit('my_event', {data: 'I\'m connected!'});
  });

  // Event handler for server sent data.
  // The callback function is invoked whenever the server emits data
  // to the client. The data is then displayed in the "Received"
  // section of the page.
  socket.on('my_response', function(msg, cb) {
    $('#log').append('<br>' + $('<div/>').text(msg.data).html());
    if (cb)
        cb();
  });
  // Interval function that tests message latency by sending a "ping"
  // message. The server then responds with a "pong" message and the
  // round trip time is measured.
  var ping_pong_times = [];
  var start_time;
  window.setInterval(function() {
      start_time = (new Date).getTime();
      $('#transport').text(socket.io.engine.transport.name);
      socket.emit('my_ping');
  }, 1000);

  // Handler for the "pong" message. When the pong is received, the
  // time from the ping is stored, and the average of the last 30
  // samples is average and displayed.
  socket.on('my_pong', function() {
      var latency = (new Date).getTime() - start_time;
      ping_pong_times.push(latency);
      ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
      var sum = 0;
      for (var i = 0; i < ping_pong_times.length; i++)
          sum += ping_pong_times[i];
      $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
  });

    // Handlers for the different forms in the page.
    // These accept data from the user and send it to the server in a
    // variety of ways
  $('form#emit').submit(function(event) {
      socket.emit('my_event', {data: $('#emit_data').val()});
      return false;
  });
  $('form#broadcast').submit(function(event) {
      socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
      return false;
  });
  $('form#join').submit(function(event) {
      socket.emit('join', {room: $('#join_room').val()});
      return false;
  });
  $('form#leave').submit(function(event) {
      socket.emit('leave', {room: $('#leave_room').val()});
      return false;
  });
  $('form#send_room').submit(function(event) {
      socket.emit('my_room_event', {room: $('#room_name').val(), data: $('#room_data').val()});
      return false;
  });
  $('form#close').submit(function(event) {
      socket.emit('close_room', {room: $('#close_room').val()});
      return false;
  });
  $('form#disconnect').submit(function(event) {
      socket.emit('disconnect_request');
      return false;
  });
});


function addUser(){
  var uIn = document.getElementById("usersADD").value;
  //var len = document.getElementById("listItem").innerHTML;
  var len = document.getElementById("noteMSG").placeholder;

  if(uIn && len){
    //document.getElementById("listItem").innerHTML += ", " + uIn;
    document.getElementById("noteMSG").placeholder += ", " + uIn;
  }
  else if(uIn){
    document.getElementById("noteMSG").placeholder = "Message: ";
    //document.getElementById("listItem").innerHTML += uIn;
    document.getElementById("noteMSG").placeholder += uIn;
  }
}

function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function editNote(noteId){ 
  n_data = prompt("Enter edited text");
  fetch("/edit-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId, note_data: n_data}),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function showPass(){
  var x = document.getElementById("password");

  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function showPass2(){
  var x = document.getElementById("password1");
  var y = document.getElementById("password2");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
  if(y.type === "password"){
    y.type = "text";
  }
  else{
    y.type = "password";
  }
}

function getMode(mode){
  if (mode === "dark"){
    document.body.style.backgroundColor = "darkgrey";
  }
  else{
    document.body.style.backgroundColor = "white";
  }
}

// using enter with messages as well as clicking submit
/*
input.addEventListener("keyup", function(event) {
    var input = document.getElementById("noteMSG").value;
    console.log(input);
    if (event.key === "Enter" && input){
        event.preventDefault();
        submit.click();
    }
}); */