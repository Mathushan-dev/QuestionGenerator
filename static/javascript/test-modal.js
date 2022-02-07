var modal = document.getElementById("testModal");

var selectedTest = document.getElementById("test");

var span = document.getElementsByClassName("close")[0];

selectedTest.onclick = function() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}
