Chart.defaults.global.defaultFontColor = "#ccc";
Chart.defaults.global.legend.labels.fontColor = "#ccc";
Chart.defaults.line = {
    showLines: true,
    scales: {
        xAxes: [
            {
                type:"category","id":"x-axis-0",
            }

        ],
        yAxes: [
            {
                type:"linear",
                "id":"y-axis-0",
                ticks: {
                    min: 0,
                    max: 3
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
labels: ['Restful', 'Non-Restful'],
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

        data: []
    }
]
};

/*****************
* DOUGHNUT CHART
******************/
var doughnutData = {
    labels: [],
    datasets: [
        {
            data: [],
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

var positionData = {
    labels: [],
    datasets: [
        {
            data: [],
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
* CHART CREATION
*******************/

var donutCtx = document.getElementById("doughnut").getContext("2d");
var donut_posCtx = document.getElementById("doughnut-pos").getContext("2d");
var lineCtx = document.getElementById("line").getContext("2d");

donutCtx.canvas.width = 400;
donutCtx.canvas.height = 350;

lineCtx.canvas.width = 400;
lineCtx.canvas.height = 300;

var lineChart = new Chart.Line(lineCtx, {
    data: lineChartData
});


var doughnutChart = new Chart(donutCtx, {
    type: 'doughnut',
    data: doughnutData
});

var positionChart = new Chart(donut_posCtx, {
    type: 'doughnut',
    data: positionData
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

             getChartDataForDay(target.date._i);
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

function clearDataFromCharts() {
    $('.error').html('You have not logged sleep for this day');
    doughnutChart.data.datasets[0].data = [];
    lineChart.data.datasets[0].data = [];

    doughnutChart.update();
    lineChart.update();

    $('#duration').html('');
    $('#efficiency').html('');
    $('#restful').html('');
     $('#non-restful').html('');
}

/*****************
* SLEEP ANALYSIS
*******************/
function getChartDataForDay(date) {
    $.ajax({
    url: "/analyzeSleepCycle",
    dataType : "json",
    data: {
        'date': date
    },
    async: false,
    success: function(response) {
        if (response['file_exists'] == false) {
            clearDataFromCharts();
            return;
        }
        else {
             $('.error').html('');
        }

        lineChartData.datasets[0].data = response['data'];
        var epochLabels = response['labels'];
        var normalLabels = [];

        // console.log(epochLabels);

        var lastDate = 0;

        for (var i = 0; i < epochLabels.length; i++) {
            var date = moment(epochLabels[i]*1000);
            // var time_only = date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
             normalLabels.push(date.format('h:mm'));
        }

        lineChartData.labels = normalLabels;

        //Update charts with new data
        doughnutChart.data.labels = [
            'Non-Restful Sleep',
            'Restful Sleep'
        ];

        doughnutChart.data.datasets = [
        {
            data: [response['total_nonrestful_time'], response['total_restful_time']],
            backgroundColor: [
                "#9b59b6",
                "#1abc9c",
                "#3498db"
            ]
        }];

        doughnutChart.update();

        lineChart.data = lineChartData;
        lineChart.update();

        var dur = response['duration'];
        var tempTime = moment.duration(dur, 'seconds');
        var y = tempTime.hours() + ' hr ' + tempTime.minutes() + ' min';
        $('#duration').html(y);
        $('#efficiency').html(response['sleep_efficiency'] + '%');

        var dur = response['restful_time'];
        var tempTime = moment.duration(dur, 'seconds');
        var y = tempTime.hours() + ' hr ' + tempTime.minutes() + ' min';
        $('#restful').html(y);

        dur = response['nonrestful_time'];
        tempTime = moment.duration(dur, 'seconds');
         var y = tempTime.hours() + ' hr ' + tempTime.minutes() + ' min';
        $('#non-restful').html(y);

        //Sleeping Position
        //Update charts with new data
        positionChart.data.labels = [
            'Front',
            'Back',
            'Right',
            'Left'
        ];

        positionChart.data.datasets = [
        {
            data: [response['position_front'], response['position_back'], response['position_right'], response['position_left']],
            backgroundColor: [
                "#9b59b6",
                "#1abc9c",
                "#3498db"
            ]
        }];

        console.log(positionChart.data.datasets);
        positionChart.update();
    }
    });

}
