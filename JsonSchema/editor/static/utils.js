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
export async function generateFileHash(file){
    // reads the file content
    const buffer = await file.arrayBuffer();
    // convert the raw data into a 256 bytes hash string
    const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    // converts each byte into a hexadecimal and then pads two zeroes to ensure each hax value is 2 characters long
    const hashIndex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashIndex;

}