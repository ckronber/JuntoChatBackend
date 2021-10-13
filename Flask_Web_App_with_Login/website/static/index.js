const socket = io();
var submit = document.getElementById("submitMessage");

socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
    console.log(socket.id);
});

socket.on("disconnect", () => {
  console.log(socket.id); // undefined
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