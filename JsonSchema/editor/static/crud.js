import { codeMirroEditor_schema }  from "./editorsetup.js";
import {codeMirroEditor_user_input}  from "./editorsetup.js";
import {websocket} from "./editorsetup.js";


function showModal() {
        var modal = document.getElementById('crud-modal');
        modal.style.display = "flex";
    }

// Function to close the modal
function closeModal() {
        var modal = document.getElementById('crud-modal');
        modal.style.display = 'none';
    }

// Function to handle saving schema
function saveSchema() {
        const schemaName = document.getElementById('schemaName').value;
        // Send schemaName to the server or perform any other action
        console.log('Schema name:', schemaName);
        console.log("data: ", codeMirroEditor_schema.getValue() )
        sendToServer({
            "event" : "SAVE",
            "schemaName" : schemaName,
            "schema" : codeMirroEditor_schema.getValue()
        })
        closeModal();
    }

// Attach functions to window object to make them global
window.showModal = showModal;
window.closeModal = closeModal;
window.saveSchema = saveSchema;

function sendToServer(data) {

    if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify(data));
      } else {
        console.error("WebSocket  not open");
      }
} 
