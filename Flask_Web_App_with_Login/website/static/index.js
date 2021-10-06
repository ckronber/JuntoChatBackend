
function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function get_edited(){
  userInput = prompt("Enter edited text");
  return userInput;
}

function editNote(noteId){ 
  n_data = get_edited();
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