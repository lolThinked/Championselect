let currentKampJsonLink = "{{url_for('getJsonDataCurrentKampJson')}}";
setInterval(async ()=>{
    if(typeof(kampData)=="object"){
        await checkKampData();
    }        
}, 5000);
async function checkKampData(){
    let xml = new XMLHttpRequest();
    console.log(currentKampJsonLink);
    xml.open("GET", currentKampJsonLink, false);  
    xml.onreadystatechange = function(){
        if(xml.readyState == 4 && xml.status == 200){
            let tempDIct = JSON.parse(xml.responseText);
            if(tempDIct!=kampData){
                window.location.reload(false);
            }
        }
    }
    xml.send();
}