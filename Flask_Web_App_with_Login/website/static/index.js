var submit = document.getElementById("submitMessage").value;
var form = document.getElementById("listItem");
var input = document.getElementById("noteMSG");
var edit = document.getElementById("edDel").outerHTML;

var listElement = document.createElement("li");
listElement.setAttribute("id", "msgEdit");

function showEditModal(){
  editModal = `
  <!-- Modal -->
  <div class="modal fade" id="editModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
      <div class="modal-header">
          <h5 class="modal-title" id="exampleModalCenterTitle">Modal title</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
          </button>
      </div>
      <div class="modal-body">
          ...
      </div>
      <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Save changes</button>
      </div>
      </div>
  </div>
  </div>
  `;
  
  $('body').append(editModal.show());
}

console.log(edit);

var username,thisUser;
const sio = io();

function scrollTobottom(){
  var objDiv = document.getElementById("messageArea");
  objDiv.scrollTop = objDiv.scrollHeight;
}

//Gets the currentUser
function getCurrentUser(){
  sio.emit("getUser");
}

$(document).ready(function() {
  sio.on("disconnect", () => {
    onlineData = 0;
    myModal.dispose()
    console.log("disconnected");
  });

  sio.on('connect', function() {
    onlineData = 1;
    console.log("connected!")
  });
  
  getCurrentUser();
  scrollTobottom();

  sio.on('c_user', function(msg) {
    username = msg.data;
  });

  sio.emit("load_all_messages");

  //message receiving message add from socketio server emit message_add
  sio.on('message_add', function(msg) {
      if(msg.id == username){
        $('#log').append("<li class='list-group-item' id = 'chatStuff'>You : "+ msg.data +"&nbsp;"+msg.edit +"</li>");
      }
      else{
        listElement = msg.user_name + " : " +  msg.data;
        $('#log').append(listElement);
      } 
      scrollTobottom()
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
  showEditModal();
  /*
  console.log('message ID: ', noteId);
  n_data = prompt("Enter edited text");
  fetch("/edit-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId, note_data: n_data}),
  }).then((_res) => {
    window.location.href = "/";
  });*/
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