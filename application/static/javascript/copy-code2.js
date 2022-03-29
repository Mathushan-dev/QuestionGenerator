function copyToClipboard(id){
    var code = document.getElementById(id).innerText;
    var element = document.createElement("textarea");
    document.body.appendChild(element);
    element.value = code
    element.select();
    document.execCommand("copy");
    document.body.removeChild(element);
}