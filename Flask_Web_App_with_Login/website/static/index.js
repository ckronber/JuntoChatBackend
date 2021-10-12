const socket = io("http://");
var input = document.getElementById("noteMSG");
var submit = document.getElementById("submitMessage")

socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
    console.log(socket.id);
});

socket.on("disconnect", () => {
  console.log(socket.id); // undefined
});

function sendMsg(messageText){
  console.log(messageText);
  return socket.emit("message", messageText);
}

/*
function sendMessage(message){
  var msgTxt = document.createElement("li");
  msgTxt.innerText = message;
  document.body.appendChild(msgTxt);
}
*/

function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

// using enter with messages as well as clicking submit
input.addEventListener("keyup", function(event) {
    if (event.key === "Enter" && input) {
        event.preventDefault();
        submit.click();
    }
});

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