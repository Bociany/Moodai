var emotion_dict = ["smutny/a", "smutny/a", "smutny/a", "szczęśliwy/a", "neutralny/a", "smutny/a", "szczęśliwy/a"];
var colors = ["red", "red", "red", "green", "orange", "red", "green"];

function drawChart(moods, ctx, title) {
	var moodLabels = [];
	var moodData = [];

	for (var i = 0; i < moods.length; i++) {
		var splitTime = moods[i].time.split('T');
		moodLabels.push(splitTime[0]);
		moodData.push(moods[i].value)
	}

    var config = {
        type: 'line',
        data: {
            labels: moodLabels,
            datasets: [{
                label: title,
                backgroundColor: 'rgb(255, 159, 64)',
                borderColor: 'rgb(255, 159, 64)',
                data: moodData,
                fill: false,
            }]
        },
        options: {
            responsive: true,
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Dzień'
                    }
                }],
                yAxes: [{
                    display: true,
                    ticks: {
                        callback: function(label, index, labels) {
                            if (label > emotion_dict.length) {
                            	return "";
                            }
                            return emotion_dict[label];
                        }
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Emocja'
                    }
                }]
            }
        }
    };

    var chart = new Chart(ctx, config);
}

doAsyncRequestMoods(7, function(data) {
	if (data.state != "ok") {
		return;
	}
	var parent = document.querySelector("#wykres-container-7");
	var sevenDays = document.querySelector("#wykres-7");
	sevenDays.width = parent.offsetWidth;
	sevenDays.height = parent.offsetHeight;

	drawChart(data.moods, sevenDays.getContext('2d'), "Samopoczucie w ciągu ostatnich 7 dni");
});

doAsyncRequestMoods(30, function(data) {
	if (data.state != "ok") {
		return;
	}
	var parent = document.querySelector("#wykres-container-30");
	var thirtyDays = document.querySelector("#wykres-30");
	thirtyDays.width = parent.offsetWidth;
	thirtyDays.height = parent.offsetHeight;

	drawChart(data.moods, thirtyDays.getContext('2d'), "Samopoczucie w ciągu ostatnich 30 dni");
});

doAsyncRequestMoods(100, function(data) {
	if (data.state != "ok") {
		return;
	}
	var parent = document.querySelector("#wykres-container-100");
	var hundredDays = document.querySelector("#wykres-100");
	hundredDays.width = parent.offsetWidth;
	hundredDays.height = parent.offsetHeight;

	drawChart(data.moods, hundredDays.getContext('2d'), "Samopoczucie w ciągu ostatnich 100 dni");
});