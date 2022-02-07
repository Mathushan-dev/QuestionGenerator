var modal2 = document.getElementById("infoModal");

var btn2 = document.getElementById("change-info-button");

var span2 = document.getElementsByClassName("close2")[0];

var window2 = window;

btn2.onclick = function() {
    modal2.style.display = "block";
}

span2.onclick = function() {
    modal2.style.display = "none";
}
