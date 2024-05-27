
var cm = null;
var cm2 = null;
document.addEventListener('DOMContentLoaded', function() {

  cm = new CodeMirror.fromTextArea(document.getElementById("schema-editor"), {
              readOnly: false,
              mode: "python",
              theme: "dracula",
              lineNumbers: true,
              matchBrackets: true,
              lineWrapping: true,
              cursorHeight: 1,
              autoCloseBrackets: true,
              styleActiveLine: true,
             
    })

    cm.setSize(480, 480);

    cm2 = new CodeMirror.fromTextArea(document.getElementById("schema-validator"), {
      readOnly: false,
      mode: "python",
      theme: "dracula",
      lineNumbers: true,
      matchBrackets: true,
      lineWrapping: true,
      cursorHeight: 1,
      autoCloseBrackets: true,
      styleActiveLine: true,
     
})

  cm2.setSize(480, 480);

});

function validate() {

  schema = cm.getValue();
  user_input = cm2.getValue();
  
  
}

// Add an event listener for when the DOM content is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Get the button element by its id
  var validator = document.getElementById('validate');

  // Attach an event listener to the button
  validator.addEventListener('click', validate);
});