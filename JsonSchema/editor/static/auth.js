


const USERNAME_REGEX = /^[a-zA-Z_$]+[a-zA0-9-Z_$]*$/;
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
export function validateForm(fieldList){
    // validate username
    var validated = true;
    fieldList.forEach(field => {

        if(field.type == "email"){
            console.log("Type of field", field.type);
            var errorSpan = field.nextElementSibling;
            if(!regexcheck(EMAIL_REGEX, field.value)){
                errorSpan.classList.remove("hidden");
                validated = false;
            }
            else{
                errorSpan.classList.add("hidden");
                validated = true;
            }
        }

        if(field.type == "password"){
            console.log("Type of field", field.type);
            var errorSpan = field.nextElementSibling;
            if(!regexcheck(PASSWORD_REGEX, field.value)){
                errorSpan.classList.remove("hidden");
                validated = false;
            }
            else{
                errorSpan.classList.add("hidden");
                validated = true;
            }
        }

        if(field.type == "text"){
            console.log("Type of field", field.type);
            var errorSpan = field.nextElementSibling;
            console.log("Error Span: ", errorSpan);
            if(!regexcheck(USERNAME_REGEX, field.value)){
                errorSpan.classList.remove("hidden");
                validated = false;

            }
            else{
                errorSpan.classList.add("hidden");
                validated = true;
            }
        }

        if(field.type == "file"){
            console.log("Type of field", field.type);
            var errorSpan = field.nextElementSibling;
            // Here we need to check for whether
            // user has uploaded a file or Not
            if(!validateFile()){
                errorSpan.classList.remove("hidden");
                validated = false;
            }
            else{
                errorSpan.classList.add("hidden");
                validated = true;
            }
        }

    });

    return validated;

}

function isEmpty(value){
    value = value.trim()
    return length(value) == 0
}

function regexcheck(regexPattern, value){
    return regexPattern.test(value)
}



export function validatePasswords(){
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

export function validateFile(){
    try {
        var file = document.getElementById('file_input').files[0];
        console.log("File: ", file);
        if(file.type != ""){
            var filetype = file.type; // mime type like image/jpeg etc
            var type = filetype.split('/')[0];
            var format = filetype.split('/')[1];
            console.log(type);
            console.log(format);
            if(!(format in ['png', 'jpeg', 'svg', 'jpg', 'gif', 'jpeg'])){
                document.getElementById("file-validation").style.display = "none";
                return true;
            }
            else{
                document.getElementById("file-validation").style.display = "block";
                return false;
            }
    }
        
    } catch (error) {
        console.log("Error Occurend", error);
        return false;
    }
}
window.validateForm = validateForm;
window.validatePasswords = validatePasswords;
window.validateFile = validateFile;


