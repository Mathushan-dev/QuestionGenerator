var modal = document.getElementById("text-modal-1");

var btn = document.getElementById("share-button");

var span = document.getElementsByClassName("close1")[0];

btn.onclick = function() {
    modal.style.display = "block";

}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}