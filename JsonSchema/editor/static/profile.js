import { validateForm } from './auth.js';

function validate(){
        console.log("Entered the form validation method in profile.js");
        event.preventDefault();
        if(validateForm([document.getElementById('username'), document.getElementById('email'), document.getElementById('file_input')])){
            console.log("Form Validated");
            var form = document.getElementById('profile-save-form');
            form.submit();
        }
        else{
            console.log("Form Validation Failed");
        }
}

window.validate = validate;