
document.addEventListener('DOMContentLoaded', function() {

  var cm = new CodeMirror.fromTextArea(document.getElementById("schema-editor"), {
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

    var cm2 = new CodeMirror.fromTextArea(document.getElementById("schema-validator"), {
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
console.log(jQuery.fn.jquery)
