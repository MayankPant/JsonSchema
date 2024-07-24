export async function getCookie(name){
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