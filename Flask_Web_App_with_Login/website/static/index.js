var submit = document.getElementById("submitMessage").value;
var form = document.getElementById("listItem");
var input = document.getElementById("noteMSG");
var username;
const sio = io();

function getCurrentUser(){
  sio.emit("getUser");
}

$(document).ready(function() {
  sio.on("disconnect", () => {
    console.log("user disconnected");
  });

  sio.on('connect', function() {
    //sio.emit('my_event', {data: 'I\'m connected!'});
    console.log("connected!")
  });

  getCurrentUser();

  sio.on('c_user', function(msg) {
    username = msg.data;
    console.log(username);
  })

  sio.emit("load_all_messages");

  // Event handler for server sent data.
  // The callback function is invoked whenever the server emits data
  // to the client. The data is then displayed in the "Received"
  // section of the page.
  sio.on('message_add', function(msg) {
    console.log(msg.id)
    if(msg.id == username){
      $('#log').append('<br>' + $('<li/>').text("You : "+ msg.data).html());
    }
    else{
      $('#log').append('<br>' + $('<li/>').text(msg.user_name +" : "+ msg.data).html());
    } 
    
      /*
          {%if current_user.first_name == note.user.first_name%}
            {{"You: " + note.data}}
            &nbsp;
            <div type = "buttimg on" id = "editB" class = "edit" onclick = "editNote('{{note.id}}')">
              <span aria-hidden = "true"><src="../static/images/edit.png" width = "20rem" height = "20rem" alt="edit"></span> 
            </div>  &nbsp;
             <div type="button" class="close" id="closeX" onclick="deleteNote('{{note.id}}')">
               <span aria-hidden="true">&times;</span>
             </div>
          {%else%} 
            {{note.user.first_name + ": " + note.data}}
          {%endif%}
        */
    });

  // Interval function that tests message latency by sending a "ping"
  // message. The server then responds with a "pong" message and the
  // round trip time is measured.

  var ping_pong_times = [];
  var start_time;
  window.setInterval(function() {
      start_time = (new Date).getTime();
      $('#transport').text(sio.io.engine.transport.name);
      sio.emit('my_ping');
  }, 1000);

  // Handler for the "pong" message. When the pong is received, the
  // time from the ping is stored, and the average of the last 30
  // samples is average and displayed.
  
  sio.on('my_pong', function() {
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
      sio.emit('my_event', {data: $('#emit_data').val()});
      return false;
  });
  $('form#broadcast').submit(function(event) {
      sio.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
      clearTextArea("broadcast_data");
      return false;
  });
  /*
  $('form#join').submit(function(event) {
      sio.emit('join', {room: $('#join_room').val()});
      return false;
  });
  $('form#leave').submit(function(event) {
      sio.emit('leave', {room: $('#leave_room').val()});
      return false;
  });
  $('form#send_room').submit(function(event) {
      sio.emit('my_room_event', {room: $('#room_name').val(), data: $('#room_data').val()});
      return false;
  });
  $('form#close').submit(function(event) {
      sio.emit('close_room', {room: $('#close_room').val()});
      return false;
  });
  */
});

function addUser(){
  var uIn = document.getElementById("usersADD").value;
  var len = document.getElementById("broadcast_data").placeholder;
  console.log(len);

  if(uIn && len){
    document.getElementById("broadcast_data").placeholder += ", " + uIn;
  }
  else if(uIn){
    document.getElementById("broadcast_data").placeholder = "Message: ";
    document.getElementById("broadcast_data").placeholder += uIn;
  }
  clearTextArea("usersADD");
}

function clearTextArea(broadcast){
  var messageData = document.getElementById(broadcast).value;
  console.log(messageData);
  messageData = "";
  document.getElementById(broadcast).value = messageData;
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
    methods: ["GET","POST"],
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