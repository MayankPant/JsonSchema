import { showToast } from "./toast.js";
async function signOut(){
    

    // clearing front end cookies.
    sessionStorage.clear();
    localStorage.clear();
    deleteAllCookies();
    try {
        var response = await fetch('/jsonschema/sign_out/');
        response = await response.json();
        if(response.status == 200){
            console.log("Signed off");
            window.location.href = '/jsonschema/login'
            showToast("Logged off.", "text-green-500");
        }
        else{
            showToast("Error Occured!", "text-red-500");
        }

    } catch (error) {
        console.log("Error Occured: ", error);
        showToast("Error Occured!", "text-red-500");
    }

}

function deleteAllCookies() {
    // manually expiring all cookies by setting their dates in the past
    document.cookie.split(';').forEach(cookie => {
      const eqPos = cookie.indexOf('=');
      const name = eqPos > -1 ? cookie.substring(0, eqPos) : cookie;
      document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
    });
  }

function toggleUserMenu(){
    var menu = document.getElementById('userMenu');
    menu.classList.toggle('hidden');
  }



window.toggleUserMenu = toggleUserMenu;
window.signOut = signOut;