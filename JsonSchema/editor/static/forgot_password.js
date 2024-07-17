import { validatePasswords } from "./auth.js";

async function showModal() {
    var modal = document.getElementById('crud-modal');
    modal.style.display = "flex";
    console.log(await generate_otp());
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
