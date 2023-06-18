
$(document).ready(()=>{
    $('.page2').hide()
    document.getElementById('file').addEventListener('change', handleFileSelect, false);
    document.getElementById('attributeSelect').addEventListener('change', function () {
        drawChart(lines, this.value);
    });
}
    
)
function mean(data){
    if(data.length==0){
        return 0;
    }
    var sum=0;
    var count=0;
    for(var i=0;i<data.length;i++){
        sum+=data[i];
        
    }
    return sum/data.length;
}
function std (array) {
    if(array.length==0){
        return 0;
    }
    const n = array.length
    const m = mean(array)
    return Math.sqrt(array.map(x => Math.pow(x - m, 2)).reduce((a, b) => a + b) / n)
  }

function handleFileSelect(event) {
    var file = event.target.files[0];
    var reader = new FileReader();
    reader.onload = function (e) {
        var contents = e.target.result;
        processData(contents);
    };
    reader.readAsText(file);
}
var headers = [];
var lines = [];
function processData(csv) {
     lines = csv.split('\n');
    headers = lines[0].split(',');
    var attributeSelect = document.getElementById('attributeSelect');
    var attributeSelectMann= document.getElementById('attributeSelectMann');
    // Clear attribute select options
    while (attributeSelect.firstChild) {
        attributeSelect.removeChild(attributeSelect.firstChild);
    }
    while (attributeSelectMann.firstChild) {
        attributeSelectMann.removeChild(attributeSelectMann.firstChild);
    }
    
    // Add headers to attribute select
    for (var i = 0; i < headers.length; i++) {
        var option = document.createElement('option');
        option.value = headers[i];
        option.text = headers[i];
        attributeSelect.appendChild(option);
    }
    for (var i = 0; i < headers.length; i++) {
        var option = document.createElement('option');
        option.value = headers[i];
        option.text = headers[i];
        attributeSelectMann.appendChild(option);
    }
    
    // Set default attribute to the first one
    attributeSelect.value = headers[0];
    try{
      chart.destroy()
    }
    
    catch(err) {
      console.log(err)
    }
    drawChart(lines, attributeSelect.value);
}

    function drawChart(lines, attribute) {
    var data = [];
    var labels = [];
    var counts = [];
    var missing = 0;
    var calData=[]
    // Process data for selected attribute
    // console.log(lines)
    var dataType='Number'
    for (var i = 1; i < lines.length; i++) {
        var values = lines[i].split(',');
        var value = (values[headers.indexOf(attribute)]);
        if (values.length==0||(values.length==1)){{
            continue;
        }}
        if(value===undefined||value===""||value===" "){
            console.log(value,i)
            missing+=1
            continue;
            }
        // Ignore NaN values
        if (isNaN(value)) {
            dataType='String'
            counts[0]++;
            continue;
        }
        //check is float
        // function isFloat(n){
        //     return Number(n) === n && n % 1 !== 0;
        // }
        // if(isFloat(value)){
        //      dataType='Float'
        // }
        value=Number(value)
        if (!counts[value]) {
            counts[value] = 1;
        } else {
            counts[value]++;
        }
        calData.push(value)
    }
    calData.sort(function (a, b) {
        
        return a - b;
        
    });
    document.getElementById("miss").innerHTML = "Missing : " + missing;
    document.getElementById("min").innerHTML = "Min : " + calData[0];
        document.getElementById("max").innerHTML = "Max : " + calData[calData.length - 1];
        document.getElementById("mean").innerHTML = "Mean : " + mean(calData).toFixed(2);
        document.getElementById("std").innerHTML = "Std : " +std(calData).toFixed(2);
        document.getElementById("dataType").innerHTML = "Type : " + dataType;
    // Convert counts object to array
    for (var key in counts) {
        if (counts.hasOwnProperty(key)) {
            data.push({
                value: Number(Number(key)),
                count: counts[key]
            });
        }
    }

    // Sort data by value in ascending order
    data.sort(function (a, b) {
        return a.value - b.value;
    });

    // If data range is within 10, display as a single bar
    if (data.length <= 10 && data[data.length - 1].value - data[0].value <= 10) {
        var singleBarData = [];
        var singleBarLabels = [];

        for (var j = 0; j < data.length; j++) {
           
            singleBarData.push(Math.round(data[j].count));
            singleBarLabels.push(Math.round(data[j].value,1));
        }

        // Chart.js configuration for single bar
        let chartStatus = Chart.getChart("chart"); // <canvas> id
            if (chartStatus != undefined) {
            chartStatus.destroy();
            }
        var ctx = document.getElementById('chart').getContext('2d');
        var chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: singleBarLabels,
                datasets: [{
                    label: 'Count',
                    data: singleBarData,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        stepSize: 1
                    }
                }
            }
        });
    } else {
        // Split data into 10 equal intervals
        var intervalSize = (data[data.length - 1].value - data[0].value) / 10;
         data.sort(function (a, b) {
            return a.value - b.value;
        });
        
        for (var k = 0; k < 10; k++) {
            var lowerBound = data[0].value + (k * intervalSize);
            var upperBound = lowerBound + intervalSize;
            var intervalCount = 0;

            for (var l = 0; l < data.length; l++) {
                var value = data[l].value;
               
                if (value >= lowerBound && value < upperBound) {
                    intervalCount += data[l].count;
                }
            }

            data.push({
                value: "["+String(Math.round(lowerBound))+","+String(Math.round(upperBound))+"]",
                count: intervalCount
            });
        }
       
        // Sort data by value in ascending order
       
        labels=[]
        counts=[]
        // Extract labels and counts for chart
        for (var m = data.length-10; m < data.length; m++) {
            labels.push(data[m].value);
            counts.push(data[m].count);
        }
        // debugger
        // Chart.js configuration for bar chart with intervals
        var ctx = document.getElementById('chart').getContext('2d');
        let chartStatus = Chart.getChart("chart"); // <canvas> id
            if (chartStatus != undefined) {
            chartStatus.destroy();
            }
        var chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Count',
                    data: counts,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        stepSize: 1
                    }
                }
            }
        });
        
    }
    }
    

