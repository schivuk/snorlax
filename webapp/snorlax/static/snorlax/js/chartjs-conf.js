var Script = function () {
var doughnutData = [
{
value: 30,
color:"#1abc9c"
},
{
value : 50,
color : "#2ecc71"
},
{
value : 100,
color : "#3498db"
},
{
value : 40,
color : "#9b59b6"
},
{
value : 120,
color : "#34495e"
}
];


var lineChartData = {
labels: ["January", "February", "March", "April", "May", "June", "July"],
datasets: [
    {
        label: "My First dataset",
        fillColor: "rgba(220,220,220,0.2)",
        strokeColor: "rgba(220,220,220,1)",
        pointColor: "rgba(220,220,220,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(220,220,220,1)",
        scaleStartValue: -5,
        data: [65, 59, 80, 81, 56, 55, 40]
    }
]
};

var lineChartOptions = {

    ///Boolean - Whether grid lines are shown across the chart
    scaleShowGridLines : true,

    //String - Colour of the grid lines
    scaleGridLineColor : "rgba(0,0,0,.05)",

    //Number - Width of the grid lines
    scaleGridLineWidth : 1,

    //Boolean - Whether to show horizontal lines (except X axis)
    scaleShowHorizontalLines: true,

    //Boolean - Whether to show vertical lines (except Y axis)
    scaleShowVerticalLines: true,

    //Boolean - Whether the line is curved between points
    bezierCurve : true,

    //Number - Tension of the bezier curve between points
    bezierCurveTension : 0.4,

    //Boolean - Whether to show a dot for each point
    pointDot : true,

    //Number - Radius of each point dot in pixels
    pointDotRadius : 4,

    //Number - Pixel width of point dot stroke
    pointDotStrokeWidth : 1,

    //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
    pointHitDetectionRadius : 20,

    //Boolean - Whether to show a stroke for datasets
    datasetStroke : true,

    //Number - Pixel width of dataset stroke
    datasetStrokeWidth : 2,

    //Boolean - Whether to fill the dataset with a colour
    datasetFill : true,

    //String - A legend template
    legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>",

    scaleOverride: true,
    scaleSteps: 3,
    scaleStepWidth: 1,
    scaleStartValue: 0,

    // scaleLabel : "<%= value = ' + foo %>"
    scaleLabel: function (valuePayload) {
        if(Number(valuePayload.value)===0)
            return '';
        if(Number(valuePayload.value)===1)
            return 'light sleep';
        if(Number(valuePayload.value)===2)
            return 'deep sleep';
        if(Number(valuePayload.value)===3)
            return 'rem sleep';
    }
};

var pieData = [{
        value : 30,
        color : "#F38630",
        label : 'Sleep',
        labelColor : 'white',
        labelFontSize : '16'
    },
    {
        value : 30,
        color : "#F34353",
        label : 'Sleep',
        labelColor : 'white',
        labelFontSize : '16'
    }];

var pieOptions = {
    toolTipTemplate : "wtf is wron with this shit",
        segmentShowStroke : true,
            segmentStrokeColor : "#fff",
            segmentStrokeWidth : 2,
            animation : true,
            animationSteps : 100,
            animationEasing : "easeOutBounce",
            animateRotate : true,
            animateScale : false,
            onAnimationComplete : null,
            labelFontFamily : "'Arial'",
            labelFontStyle : "normal",
            labelFontSize : 12,
            labelFontColor : "#666",
};

var barChartData = {
labels : ["January","February","March","April","May","June","July"],
datasets : [
{
fillColor : "rgba(220,220,220,0.5)",
strokeColor : "rgba(220,220,220,1)",
data : [65,59,90,81,56,55,40]
},
{
fillColor : "rgba(151,187,205,0.5)",
strokeColor : "rgba(151,187,205,1)",
data : [28,48,40,19,96,27,100]
}
]
};
var chartData = [
{
value : Math.random(),
color: "#D97041"
},
{
value : Math.random(),
color: "#C7604C"
},
{
value : Math.random(),
color: "#21323D"
},
{
value : Math.random(),
color: "#9D9B7F"
},
{
value : Math.random(),
color: "#7D4F6D"
},
{
value : Math.random(),
color: "#584A5E"
}
];
var radarChartData = {
labels : ["","","","","","",""],
datasets : [
{
fillColor : "rgba(220,220,220,0.5)",
strokeColor : "rgba(220,220,220,1)",
pointColor : "rgba(220,220,220,1)",
pointStrokeColor : "#fff",
data : [65,59,90,81,56,55,40]
},
{
fillColor : "rgba(151,187,205,0.5)",
strokeColor : "rgba(151,187,205,1)",
pointColor : "rgba(151,187,205,1)",
pointStrokeColor : "#fff",
data : [28,48,40,19,96,27,100]
}
]
};

$.ajax({
    url: "/analyzeSleepCycle",
    dataType : "json",
    async: false,
    success: function(response) {
        lineChartData.datasets[0].data = response['data'];
        var epochLabels = response['labels'];
        var normalLabels = [];

        for (var i = 0; i < epochLabels.length; i++) {
            var date = new Date(epochLabels[i]*1000);
            var time_only = date.getHours() + ":" + date.getMinutes();
            normalLabels.push(time_only);
        }

        lineChartData.labels = normalLabels;

        doughnutData = [
        {
            value: response['total_light_time'],
            color: '#0000FF',
            label: 'Light Sleep'
        },
        {
            value: response['total_deep_time'],
            color: '#00FF00',
            label: 'Deep Sleep'
        },
        {
            value: response['total_rem_time'],
            color: '#FF0000',
            label: 'REM Sleep'
        }
        ]
    }
});

var doughnut = new Chart(document.getElementById("doughnut").getContext("2d")).Doughnut(doughnutData);
document.getElementById('js-legend').innerHTML = doughnut.generateLegend();
new Chart(document.getElementById("line").getContext("2d")).Line(lineChartData, lineChartOptions);
new Chart(document.getElementById("radar").getContext("2d")).Radar(radarChartData);
new Chart(document.getElementById("polarArea").getContext("2d")).PolarArea(chartData);
new Chart(document.getElementById("bar").getContext("2d")).Bar(barChartData);
new Chart(document.getElementById("pie").getContext("2d")).Pie(pieData, pieOptions);
}();