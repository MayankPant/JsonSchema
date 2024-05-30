var cm = null;
var cm2 = null;
let schema = null;
let user_input = null;
let websocket = null;

document.addEventListener('DOMContentLoaded', function() {
  cm = new CodeMirror.fromTextArea(document.getElementById("schema"), {
    readOnly: false,
    mode: "python",
    theme: "dracula",
    lineNumbers: true,
    matchBrackets: true,
    lineWrapping: true,
    cursorHeight: 1,
    autoCloseBrackets: true,
    styleActiveLine: true,
  });
  cm.setSize(480, 480);

  cm2 = new CodeMirror.fromTextArea(document.getElementById("user-input"), {
    readOnly: false,
    mode: "python",
    theme: "dracula",
    lineNumbers: true,
    matchBrackets: true,
    lineWrapping: true,
    cursorHeight: 1,
    autoCloseBrackets: true,
    styleActiveLine: true,
  });
  cm2.setSize(480, 480);

  // Open WebSocket connection when the page loads
  openConnection();
});

function openConnection(){
  schema = cm.getValue();
  console.log("schema " + schema);
  user_input = cm2.getValue();  
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
    cm.setValue(responseData.response);
  };
  // sends the data to the server from client
  cm.on('change', sendToServer);
}

function sendToServer(){
  schema = cm.getValue();
  user_input = cm2.getValue();
  
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
