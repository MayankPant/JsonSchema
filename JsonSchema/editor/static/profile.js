import { validateForm, validateFile } from './auth.js';
import { showToast, hideToast, updateToast } from './toast.js';
import { getCookie, generateFileHash } from './utils.js';
import { uploadImage } from './signup.js'
const cloudName  = 'dgmgf7uua'

async function editProfile() {
    const csrf_token = getCookie("csrf_token");
    console.log("Entered the edit profile function.");
    var form = document.getElementById('profile-save-form');
    showToast("Profile Updated!", "text-green-500");
    form.submit();
}

async function validateAndUpload(){
    console.log("Entered the form validation method in profile.js");
        event.preventDefault();
        if(validateForm([document.getElementById('username'), document.getElementById('email'), document.getElementById('file_input')])){
            console.log("Form Validated");
            
            var file = document.getElementById('file_input').files[0];
            console.log("File: ", file);
            var formData = new FormData(document.getElementById('profile-save-form'));
            const checkFileExists = await checkResource(file);
            if (checkFileExists != null){
                formData.append('cloudinary_public_id', checkFileExists.public_id);
                const file_hash = await generateFileHash(file);
                // generating file hash again because we need this in view
                formData.append('profile_picture_file_hash',file_hash);
                formData.delete('profile_picture');
                showToast("File already exists", "text-blue-500");
            }
            else{
                const public_id = await uploadImage(document.getElementById("file_input").files[0]);
                updateTheCurrentImage(public_id);
                formData.append('cloudinary_public_id', checkFileExists.public_id);
                const file_hash = await generateFileHash(file);
                formData.append('profile_picture_file_hash', file_hash);
                formData.delete('profile_picture');
            }
        }
        else{
            showToast("Bad Credentials.", "text-red-500");
            console.log("Form Validation Failed");
        }
}

async function checkResource(file){
    /**
     * 
     * Checks for whether the file exists within the server or not.
     * Compares the file hash of the currently loaded image with the image in
     * the database if it exists.
     * 
     */
    const currentFileHash = await generateFileHash(file);
    console.log("Current uploaded file hash: ", currentFileHash);
    var response = await fetch('/jsonschema/check_file_exists/', {
        method: 'POST',
        body: JSON.stringify({
            
                "uploaded_file_hash" : currentFileHash
            
        })
    })
    response = await response.json();

    if(response.status == 200){
        console.log("File already exists");
        return response.public_id;
    }
    else{
        console.log("File not found");
        return null;
    }

}
function updateTheCurrentImage(publicId){
    var profile_picture = document.getElementById('profile_picture');
    var image_url = `https://res.cloudinary.com/${cloudName}/image/upload/${publicId}`;
    profile_picture.src = image_url;
}
window.validateAndUpload = validateAndUpload;
window.editProfile = editProfile;