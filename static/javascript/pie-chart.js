var ctx = document.getElementById("myChart").getContext('2d');

var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ["True", "False"],
        datasets: [{    
            data: [15, 5], // Specify the data values array
          
            borderColor: ['#064635', '#9B0000'], // Add custom color border 
            backgroundColor: ['#519259', '#FF7272'], // Add custom color background (Points and Fill)
            borderWidth: 1 // Specify bar border width
        }]},         
    options: {
      responsive: true, // Instruct chart js to respond nicely.
      maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height 
    }
});