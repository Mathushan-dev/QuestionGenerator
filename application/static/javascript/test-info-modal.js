var modal = document.getElementById("myModal");

var btn = document.getElementById("test");

var span = document.getElementsByClassName("close")[0];

function writeInModal(attempts, context, options, date){
    var texts = [("Attempts: " + attempts), ("Context: " + context), ("Options: " + options), ("Date Taken: " + date)];
    var elements = modal.getElementsByClassName("modalText");
    for(var i = 0; i<elements.length; i++){
        var current = elements[i];
        current.innerHTML = texts[i];
    }
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