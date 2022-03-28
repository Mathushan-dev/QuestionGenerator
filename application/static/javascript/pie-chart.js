var ctx = document.getElementById("myChart").getContext('2d');

var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ["True", "False"],
        datasets: [{    
            data: [25,5],
          
            borderColor: ['#006400', '#FF0000', '#006400', '#FF0000'], // Add custom color border 
            backgroundColor: ['#228B22', '#FF6347', '#228B22', '#FF6347'], // Add custom color background (Points and Fill)
            borderWidth: 1 // Specify bar border width
        }]},         
    options: {
      responsive: true, // Instruct chart js to respond nicely.
      maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height 
    }
});