export var codeMirroEditor_schema = null;
export var codeMirroEditor_user_input = null;
var schema = null;
var user_input = null;
export var websocket = null;

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
  console.log("schema instance created");

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
  console.log("user instance created");
  

  // Open WebSocket connection when the page loads
  openConnection();
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
  websocket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    console.log(data);
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

