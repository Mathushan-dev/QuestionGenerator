var modal = document.getElementById("myModal");

var link = document.getElementById("terms-conditions");

var span = document.getElementsByClassName("close")[0];

link.onclick = function() {
    modal.style.display = "block";
  }

span.onclick = function() {
    modal.style.display = "none";
  }
  
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
  