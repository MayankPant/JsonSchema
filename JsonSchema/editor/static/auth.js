
import { websocket } from "./editorsetup";

const USERNAME_REGEX = /^[a-zA-Z0-9_$]{1,200}$/;
const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,}$/;

/**
 * 
This regular expression checks for the following:

At least one lowercase letter ((?=.*[a-z]))
At least one uppercase letter ((?=.*[A-Z]))
At least one digit ((?=.*\d))
At least one special character ((?=.*[@$!%*?&_]))
Total length of at least 8 characters ({8,})

 */
function validateForm(){
    // validate username

    var username = document.getElementById("username");
    var email = document.getElementById('email');
    var password = document.getElementById('password');
    var confirm_password = document.getElementById('confirm_password');

    if  (!(regexcheck(USERNAME_REGEX, username.value) && isEmpty(username.value))){
        document.getElementById('username_flagger').innerHTML("Please enter a valid username.")
    }

}

function isEmpty(value){
    value = value.trim()
    return length(value) == 0
}

function regexcheck(regexPattern, value){
    return regexPattern.test(value)
}

function flagError(message, domObject){
    
}

function validatePasswords(){
    var password = document.getElementById('password');
    var confirm_password = document.getElementById('confirm_password');

    if(password.value == confirm_password.value){
        document.getElementById("password-validation").style.display = "none";
        return true;
    }
    else{
        document.getElementById("password-validation").style.display = "block";
        return false;
    }
}

function validateFile(){
    var file = document.getElementById('file_input').files[0];
    if(file.type != ""){
        var filetype = file.type; // mime type like image/jpeg etc
        var type = filetype.split('/')[0];
        var format = filetype.split('/')[1];
        console.log(type)
        console.log(format)
        if(!(format in ['png', 'jpeg', 'svg', 'jpg', 'gif'])){
            document.getElementById("file-validation").style.display = "block";
            return true;
        }
        else{
            document.getElementById("file-validation").style.display = "none";
            return false;
        }
    }
}
function otpVerification(){
    
    if (validatePasswords()){
        dataToBeSent = {
            "event" : "generate_and verify_otp",
            "length" : 4,
        }

        if (websocket && websocket.readyState === WebSocket.OPEN) {
            websocket.send(JSON.stringify(dataToBeSent));
          } else {
            console.error("WebSocket  not open");
          }

    }
}