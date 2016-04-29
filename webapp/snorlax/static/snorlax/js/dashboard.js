
/***********************
 * CHART CONFIGURATION
 **********************/
 var lineChartOptions = {
    ///Boolean - Whether grid lines are shown across the chart
    scaleShowGridLines : false,

    //String - Colour of the grid lines
    scaleGridLineColor : "#000",

    //Number - Width of the grid lines
    scaleGridLineWidth : 1,

    scaleFontColor : "#ccc",

    backgroundColor: "#ccc",

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

    responsive: true,

// Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container

    maintainAspectRatio: false,
    //String - A legend template
    legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>",

    scaleOverride: true,
    scaleSteps: 3,
    scaleStepWidth: 1,
    scaleStartValue: 0,

    // scaleLabel : "<%= value = ' + foo %>"
    scaleLabel: function (valuePayload) {
        console.log(Number(valuePayload));
        if(Number(valuePayload.value)===0)
            return '';
        if(Number(valuePayload.value)===1)
            return 'light sleep';
        if(Number(valuePayload.value)===2)
            return 'deep sleep';
        if(Number(valuePayload.value)===3)
            return 'rem sleep';
    },

};

Chart.defaults.global.defaultFontColor = "#ccc";
Chart.defaults.global.legend.labels.fontColor = "#ccc";
Chart.defaults.line = {
    showLines: true,
    scales: {
        xAxes: [
            {type:"category","id":"x-axis-0"}
        ],
        yAxes: [
            {
                type:"linear",
                "id":"y-axis-0",
                ticks: {
                    beginAtZero:true,
                    max: 4
                }
            }
        ],
    }
};

/***********************
 * INITIALIZE PLOTS
 **********************/

/*****************
* LINE CHART
******************/
var lineChartData = {
labels: ["January", "February", "March", "April", "May", "June", "July"],
datasets: [
    {
            label: "Sleep Analysis",
            fill: true,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 3.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            scaleStartValue: -5,

        data: [1, 2, 3, 4, 3, 2, 1]
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

/*****************
* DOUGHNUT CHART
******************/
var doughnutData = {
    labels: [
        "Red",
        "Green",
        "Yellow"
    ],
    datasets: [
        {
            data: [300, 50, 100],
            backgroundColor: [
                "#FF6384",
                "#36A2EB",
                "#FFCE56"
            ],
            hoverBackgroundColor: [
                "#FF6384",
                "#36A2EB",
                "#FFCE56"
            ]
        }]
};

/*****************
* RADAR CHART
******************/
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

/*****************
* BAR CHART
******************/
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

/*****************
* CHART CREATION
*******************/

var donutCtx = document.getElementById("doughnut").getContext("2d");
var lineCtx = document.getElementById("line").getContext("2d");
var radarCtx = document.getElementById("radar").getContext("2d");
var polarCtx = document.getElementById("polarArea").getContext("2d");

donutCtx.canvas.width = 400;
donutCtx.canvas.height = 300;

lineCtx.canvas.width = 400;
lineCtx.canvas.height = 300;


radarCtx.canvas.width = 400;
radarCtx.canvas.height = 300;

polarCtx.canvas.width = 400;
polarCtx.canvas.height = 300;

// var doughnutChart = new Chart(donutCtx).Doughnut(doughnutData);
// var lineChart = new Chart(lineCtx).Line(lineChartData, lineChartOptions);
// var doughnutChart = null;
// var lineChart = null;
// var radarChart = new Chart(radarCtx).Radar(radarChartData);
// var polarChart = new Chart(polarCtx).PolarArea(chartData);
var lineChart = new Chart(lineCtx, {
    type: 'line',
    data: lineChartData,
    // options: lineChartOptions
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:false
                }
            }]
        },
        scaleLabel: function (valuePayload) {
            console.log(Number(valuePayload));
            if(Number(valuePayload.value)===0)
                return '';
            if(Number(valuePayload.value)===1)
                return 'light sleep';
            if(Number(valuePayload.value)===2)
                return 'deep sleep';
            if(Number(valuePayload.value)===3)
                return 'rem sleep';
        }
    }
});

var doughnutChart = new Chart(donutCtx, {
    type: 'doughnut',
    data: doughnutData
});

/**************************
 * CALENDAR CONFIGURATION
 *************************/

// Calendar helper function
function weeksInMonth(month) {
    return Math.floor((month.daysInMonth() + moment(month).startOf('month').weekday()) / 7);
}

var clndr = $('#cal').clndr({
    template: $('#template-calendar').html(),
    extras: {
        currentWeek: Math.floor( ( ( (moment().date() + moment().startOf('month').weekday() ) - 1 ) / ( weeksInMonth(moment() ) * 7) ) * weeksInMonth( moment() ) )
    },
    clickEvents: {
    click: function(target) {

              //Set color for active date
              var prev = $('.activeDate');
              if(prev !== null) {
                prev.removeClass('activeDate');
              }
              var div = $(target['element']);
              div.addClass('activeDate');

             getChartDataForDay(target);
             // console.log(doughnutData);


        }
    },
    doneRendering: function() {

        /* Next button handler */
        $('.clndr-next-but').on('click', function() {

            /* Get numbers of weeks in the month */
            var weeks_in_month = Math.floor(clndr.month.daysInMonth() / 7) - 1;

            if(clndr.options.extras.currentWeek <= weeks_in_month) {
                /* Increase the week count */
                clndr.options.extras.currentWeek += 1;
            } else {
                /* Reset the week count */
                clndr.options.extras.currentWeek = 0;

                /* Go to next month */
                clndr.next();
            }

            clndr.render();
        });

        /* Previous button handler */
        $('.clndr-previous-but').on('click', function() {

            /* Get numbers of weeks in the month */
            var weeks_in_month = Math.floor(clndr.month.daysInMonth() / 7) - 1;


            if(clndr.options.extras.currentWeek > 0) {
                /* Decrease the week count */
                clndr.options.extras.currentWeek -= 1;
            } else {
                /* Reset the week count */
                clndr.options.extras.currentWeek = weeks_in_month;

                /* Go to previous month */
                clndr.back();
            }

            clndr.render();
        });

    }
});


/*****************
* SLEEP ANALYSIS
*******************/
function getChartDataForDay(date) {
    console.log('getChartDataForDay');

    $.ajax({
    url: "/analyzeSleepCycle",
    dataType : "json",
    async: false,
    success: function(response) {
        lineChartData.datasets[0].data = response['data'];
        var epochLabels = response['labels'];
        var normalLabels = [];

        // console.log(epochLabels);

        for (var i = 0; i < epochLabels.length; i++) {
            var date = new Date(epochLabels[i]*1000);
            var time_only = date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
            normalLabels.push(time_only);
        }

        lineChartData.labels = normalLabels;

        //Update charts with new data
        doughnutChart.data.labels = [
            'Nonrestful Sleep',
            'Restful Sleep'
        ];

        doughnutChart.data.datasets = [
        {
            data: [response['total_nonrestful_time'], response['total_restful_time']],
            backgroundColor: [
                "#9b59b6",
                "#1abc9c",
                "#3498db"
            ],
            hoverBackgroundColor: [
                "#FF6384",
                "#36CEAD",
                "#FFCE56"
            ]
        }];

        doughnutChart.update();
        console.log(doughnutChart);

        lineChart.data = lineChartData;
        lineChart.update();
    }
    });

}
