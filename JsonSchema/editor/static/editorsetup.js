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

  websocket.onopen =  function(event){
    console.log('WebSocket is open now.');
    // Send acknowledgment message to the backend
    /**
     * The issue we were facing when sending the user details to the frontend
     * was that even before a connection was establised, we were sending in
     * the information which of-course caused it to miss it. So what we did was
     * onnly when a the websocket connection was establised we sent in an acknowledgement
     * message to the server, and only then the server sent the the user information
     * This was done through recieve and send_user_data in the consumer.
     * 
     */
    websocket.send(JSON.stringify({
        type: 'websocket_acknowledgement',
        message: 'WebSocket connection established'
    }));
  };

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

