import { validateForm } from './auth.js';
import { showToast, hideToast, updateToast } from './toast.js';
function validate(){
        console.log("Entered the form validation method in profile.js");
        event.preventDefault();
        if(validateForm([document.getElementById('username'), document.getElementById('email'), document.getElementById('file_input')])){
            console.log("Form Validated");
            showToast("Profile Updated", "text-green-500");
            var form = document.getElementById('profile-save-form');
            form.submit();
        }
        else{
            showToast("Bad Credentials.", "text-red-500");
            console.log("Form Validation Failed");
        }
}

window.validate = validate;