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
        location.reload();
    }

    /**
     * here since radio buttons are designed to be grouped within
     * the same for and in here we have multiple forms, we need
     * to manually change the state of radio buttons using javascript
     * 
     */
// Get all radio buttons with class 'radio-schemas' across all forms
var radios = document.querySelectorAll('.radio-schemas');

// Add a change event listener to each radio button
radios.forEach(function(radio) {
    radio.addEventListener('change', function() {
        // When a radio button is selected, unselect all others
        radios.forEach(function(otherRadio) {
            if(otherRadio !== radio) {
                otherRadio.checked = false;
            }
        });
    });
});

/**
 * On select of a particular schema, it should be viewed in the
 * Json schema editor window. We also Added a few lines of code
 * to beautify the code before setting up the codeeditor value.
 * 
 */
function viewSchema(){
    console.log("View Schema event");
        var radios = document.getElementsByName("selected_schema")
        radios.forEach(function(radio){
            if(radio.checked){
                var schema_name = radio.value;
                console.log("Current schema selected: " + schema_name)
                var user_schemas = sessionStorage.getItem("user_schemas");

            if (!user_schemas) {
                console.error("user_schemas not found in sessionStorage");
                return;
            }

            try {
                user_schemas = JSON.parse(user_schemas);
            } catch (e) {
                console.error("Error parsing user_schemas from sessionStorage", e);
                return;
            }

            for(let i = 0; i < user_schemas.length; i++){
                if(user_schemas[i].schema_name == schema_name)
                    try {
                        let prettyJsonString = JSON.stringify(JSON.parse(user_schemas[i].schema_text), null, 2);
                        console.log(prettyJsonString);
                        codeMirroEditor_schema.setValue(prettyJsonString);
                        // Alternatively, if using CodeMirror 6:
                        // codeMirroEditor_schema.dispatch({
                        //     changes: { from: 0, insert: prettyJsonString }
                        // });
                    } catch (e) {
                        console.error("Error parsing JSON:", e);
                    }
            }
                
            }
        });
}

// Attach functions to window object to make them global
window.showModal = showModal;
window.closeModal = closeModal;
window.saveSchema = saveSchema;
window.viewSchema = viewSchema;

function sendToServer(data) {

    if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify(data));
      } else {
        console.error("WebSocket  not open");
      }
} 
