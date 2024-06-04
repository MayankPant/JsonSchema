var codeMirroEditor_schema = null;
var codeMirroEditor_user_input = null;
let schema = null;
let user_input = null;
let websocket = null;

document.addEventListener('DOMContentLoaded', function() {
  codeMirroEditor_schema = new CodeMirror.fromTextArea(document.getElementById("schema"), {
    readOnly: false,
    mode: "application/json",
    theme: "dracula",
    lineNumbers: true,
    matchBrackets: true,
    lineWrapping: true,
    cursorHeight: 1,
    autoCloseBrackets: true,
    styleActiveLine: true,
    gutters: ["Codemirror-lint-markers"],
    lint: true,
    
  });
  codeMirroEditor_schema.setSize(480, 480);

  codeMirroEditor_user_input = new CodeMirror.fromTextArea(document.getElementById("user-input"), {
    readOnly: false,
    mode: "application/json",
    theme: "dracula",
    lineNumbers: true,
    matchBrackets: true,
    lineWrapping: true,
    cursorHeight: 1,
    autoCloseBrackets: true,
    styleActiveLine: true,
    gutters: ["Codemirror-lint-markers"],
    lint: true,
    
  });

  codeMirroEditor_user_input.setSize(480, 480);

  // Open WebSocket connection when the page loads
  openConnection();
  setAvatar();
});

function openConnection(){
  schema = codeMirroEditor_schema.getValue();
  console.log("schema " + schema);
  user_input = codeMirroEditor_user_input.getValue();  
  console.log("User Input " + user_input);

  websocket = new WebSocket(
    "ws://" + 
    window.location.host +
    "/ws/verify/"
  );

  websocket.addEventListener('open', function(event){
    console.log("Websocket is connected");
  });

  // receiving a message from server to client
  websocket.onmessage = function(event){
    console.log("Message from server: ", event.data);
    const responseData = JSON.parse(event.data);
    codeMirroEditor_schema.setValue(responseData.response);
  };
  // sends the data to the server from client
  codeMirroEditor_schema.on('change', sendToServer);
}

function sendToServer(){
  schema = codeMirroEditor_schema.getValue();
  user_input = codeMirroEditor_user_input.getValue();
  
  const data = {
    "schema": schema,
    "user_input": user_input
  };

  if (websocket && websocket.readyState === WebSocket.OPEN) {
    websocket.send(JSON.stringify(data));
  } else {
    console.error("WebSocket is not open");
  }
}

function toggleUserMenu(){
  var menu = document.getElementById('userMenu');
  menu.classList.toggle('hidden');
}

function setAvatar(){
  var avatar  = document.getElementById("avatar");
  
}