import { validateForm, validateFile } from './auth.js';
import { showToast, hideToast, updateToast } from './toast.js';
import { getCookie } from './utils.js';
const api_key = '127513444384144' 
const cloud_name  = 'dgmgf7uua'

async function submitForm(){
    event.preventDefault();
    var formData = new FormData(document.getElementById('profile-save-form'));
    
    /**
     * No longer need the profile picture file as it is already uploaded
     * to cloud with its public id incorporated into the cloudniaryPublicId
     * hidden field. So no need to send the file to server.
     */
    
    formData.delete('profile-picture');
    const csrf_token = await getCookie("csrftoken");
    var subission_response = await fetch("/jsonschema/signup/",{
        method: 'POST',
        mode: "cors",
        headers: {
            "X-CSRFToken": csrf_token
        },
        credentials: "same-origin",
        body: formData,
    })

    subission_response = await subission_response.json();
    if(subission_response.status == 200){
        showToast("Profile Updated", "text-green-500");
        window.location.href='/jsonschema/login';
    }
    else{
        showToast("Bad or duplicate credentials.", "text-red-500");
    }
}

async function validate(){
        console.log("Entered the form validation method in profile.js");
        event.preventDefault();
        if(validateForm([document.getElementById('username'), document.getElementById('email'), document.getElementById('file_input')])){
            console.log("Form Validated");
            
            var file = document.getElementById('file_input').files[0];
            console.log("File: ", file);
            await uploadImage(file);
        }
        else{
            showToast("Bad Credentials.", "text-red-500");
            console.log("Form Validation Failed");
        }
}
async function uploadImage(file) {
    if (!validateFile()) {
        showToast("Invalid file.", 'text-red-500');
        return;
    }

    try {
        showToast("Uploading file...", 'text-blue-500');

        const csrf_token = await getCookie("csrftoken");
        const signatureResponse = await fetch('/jsonschema/get_signature', {
            method: 'GET',
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token
            },
            credentials: "same-origin",
        });

        if (!signatureResponse.ok) {
            throw new Error(`HTTP error! status: ${signatureResponse.status}`);
        }
        const signatureData = await signatureResponse.json();
    
        const formData = new FormData();
        formData.append('file', file);
        formData.append('api_key', signatureData.api_key);
        formData.append('timestamp', signatureData.timestamp);
        formData.append('signature', signatureData.signature);
        formData.append('folder', 'jsonschema_profiles');
        
        const uploadResponse = await fetch(`https://api.cloudinary.com/v1_1/${cloud_name}/image/upload`, {
            method: 'POST',
            body: formData
        });

        if (!uploadResponse.ok) {
            throw new Error(`HTTP error! status: ${uploadResponse.status}`);
        }
        const uploadResult = await uploadResponse.json();
        
        console.log('Upload successful: ', uploadResult.secure_url);
        document.getElementById('cloudinaryPublicId').value = uploadResult.public_id;
        showToast("File successfully uploaded.", 'text-green-500');
    } catch (error) {
        console.error("Error while uploading file: ", error);
        showToast("File upload failed.", 'text-red-500');
    }
}
window.validate = validate;
window.uploadImage = uploadImage;
window.submitForm = submitForm;