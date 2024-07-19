import { validatePasswords } from "./auth.js";
import { showToast, hideToast, updateToast } from "./toast.js";

async function showModal() {
    try {
        if(!validatePasswords()){
            var password_warning = document.getElementById("password-validation");
            password_warning.classList.remove("hidden");
            return;
        }
        // adding a loader ring dynamically
        var loader_ring = document.getElementById("verify_button");
        loader_ring.innerHTML = `
        <svg aria-hidden="true" role="status" class="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
        <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
        </svg> VERIFY
        `;

        var response = await generate_otp();
        console.log("Returned Response: ", response);
        if(response == 200){
            updateToast("OTP Generated", "text-green-500");
            showToast("OTP Generated", "text-green-500");
            var modal = document.getElementById('crud-modal');
            modal.style.display = "flex";
        } else {
            updateToast("Bad Credentials.", "text-red-500");
            showToast("Bad Credentials.", "text-red-500");
        }
    } catch (error) {
        console.error("Error in showModal:", error);
        updateToast("An error occurred", "text-red-500");
        showToast("An error occurred", "text-red-500");
    } finally {
        document.getElementById("verify_button").innerHTML = `VERIFY`;
    }
}

async function getCookie(name){
    let cookieValue = null;
    if(document.cookie && document.cookie !== ''){
        const cookies = document.cookie.split(";");
        console.log("Cookie List ",cookies);
        for(let i = 0; i < cookies.length; i++){
            const cookie = cookies[i].trim();
            console.log("CSRF TOKEN ", cookie);

            if(cookie.substring(0, name.length + 1) === (name + "=")){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                console.log("Returned Cookie Value ", cookieValue);
                break;
            }
        }
    }

    return cookieValue;
}
async function generate_otp(){

    const url = "/jsonschema/generate_otp/"
    console.log("OTP Mail: ", document.getElementById("email").value)
    const data = {
        "event" : "GENERATE_OTP",
        "user_email" : document.getElementById("email").value,
        "length" : 6
    }
    const csrf_token = await getCookie("csrftoken");
    console.log("Retrieved CSRF Token ", csrf_token);
    const response =  await fetch(url, {
        method : "POST",
        mode: "cors",
        headers: {
            "Content-Type" : "application/json",
            "X-CSRFToken": csrf_token
        },
        body : JSON.stringify(data),
        credentials: "same-origin",
    });

    return response.json();
}
// Function to close the modal
function closeModal() {
    var modal = document.getElementById('crud-modal');
    modal.style.display = 'none';
}

// use this simple function to automatically focus on the next input
function focusNextInput(el, prevId, nextId) {
    if (el.value.length === 0) {
        if (prevId) {
            document.getElementById(prevId).focus();
        }
    } else {
        if (nextId) {
            document.getElementById(nextId).focus();
        }
    }
}

document.querySelectorAll('[data-focus-input-init]').forEach(function(element) {
    element.addEventListener('keyup', function() {
        const prevId = this.getAttribute('data-focus-input-prev');
        const nextId = this.getAttribute('data-focus-input-next');
        focusNextInput(this, prevId, nextId);
    });
});

window.showModal = showModal;
window.closeModal = closeModal;
window.generate_otp = generate_otp;
window.validatePasswords = validatePasswords;
