var ctx = document.getElementById("report").getContext('2d');

var data = [15, 5];
var labels = ["Correct", "Incorrect"];

var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Answers',
            data: data, // Specify the data values array
            backgroundColor: [ // Specify custom colors
                '#064635',
                '#9B0000',
            ],
            borderColor: [ // Add custom color borders
                '#519259',
                '#FF7272',
            ],
            borderWidth: 1 // Specify bar border width
        }]
    },
    options: {
      responsive: true, // Instruct chart js to respond nicely.
      maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height 
    }
});