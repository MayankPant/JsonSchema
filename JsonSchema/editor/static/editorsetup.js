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
    linseWrapping: true,
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
  disableEditorBorders(); // disables the borders for the editor
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
    console.log("Recieved Data: " + JSON.stringify(data))

    switch(data.event){
      case "editor_change":

        if (data.Validation == "True"){
          console.log("Changing borders on True");
          var editorBorders = document.querySelectorAll('.cm-s-dracula.CodeMirror');
          editorBorders.forEach(function(border) {
            border.style.border = "7px solid";
            border.style.borderImage = "linear-gradient(45deg, #90ee90, #00ff00, #90ee90) 1 / 1 / 0 stretch";
            border.style.borderRadius = "4px";
          });
        }
        else if (data.Validation == "False"){
          console.log("Changing borders on False");
          var editorBorders = document.querySelectorAll('.cm-s-dracula.CodeMirror');
          editorBorders.forEach(function(border) {
            border.style.border = "7px solid";
            border.style.borderImage = "linear-gradient(45deg, #f80808, #ff3333, #f80808) 1 / 1 / 0 stretch";
            border.style.borderRadius = "4px";
          });
        }
        break;
      
        case "send_user_data_event":
          sessionStorage.setItem("user", JSON.stringify(data.user_data.user));
          console.log("User schemas: " + console.log(data.user_data.user_schemas));
          sessionStorage.setItem("user_schemas", JSON.stringify(data.user_data.user_schemas));
          console.log(sessionStorage.getItem("user_schemas"));
          break;

    }
  };
  
  // sends the data to the server from client
  codeMirroEditor_schema.on('change', sendToServer);
  codeMirroEditor_user_input.on('change', sendToServer);
}

function disableEditorBorders(){
  var editorBorders = document.querySelectorAll('.cm-s-dracula.CodeMirror');
  editorBorders.forEach(function(border) {
    border.style.border = "None";
  })
}

function sendToServer(){
  schema = codeMirroEditor_schema.getValue();
  user_input = codeMirroEditor_user_input.getValue();
  
  const data = {
    "event" :  "editor_change",
    "schema": schema,
    "user_input": user_input
  };

  if (websocket && websocket.readyState === WebSocket.OPEN) {
    websocket.send(JSON.stringify(data));
  } else {
    console.error("WebSocket is not open");
  }
}


