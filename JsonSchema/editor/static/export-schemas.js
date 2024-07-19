async function exportSchemas(){
    console.log("Export Schema Started");
    var url = "/jsonschema/export_schemas/"
    const csrf_token = getCookie("csrftoken");
    console.log("Retrieved CSRF Token ", csrf_token);
    var response = await fetch(url,
        {
            "method" : "GET",
            "mode" : "cors",
            "headers" : {
                "Content-Type" : "application/json",
                "X-CSRFToken" : csrf_token
            }
        }
    ).catch(error => console.error('Error', error));


    console.log("Returned Data: ", response);
    response = await response.json();
    const jsonString = JSON.stringify(response, null, 2);
    const blob = new Blob([jsonString], {type: "application/json"});
    console.log("Blob object: ", blob);
    url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = 'user_schema.json';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);

}

function getCookie(name){
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

window.exportSchemas = exportSchemas;