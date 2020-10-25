var token = "" || window.localStorage.getItem("token") || window.sessionStorage.getItem("token");

function doAsyncLogout() {
    fetch('/api/logout', {
        method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
        body: new URLSearchParams({'token': token})
    }).then(response => response.json())
      .then(function(data) {
      	console.log(data)
        if (data.state == "ok") {
        	window.localStorage.removeItem("token");
        	window.sessionStorage.removeItem("token");
            window.location.replace("/");
        }
      });
}

function doAsyncServerHello() {
	fetch ('/api/hello', {
		method: 'POST',
		headers: {
        	'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        	'Authorization': 'Bearer ' + token
        },
        body: new URLSearchParams({'token': token})
	}).then(response => response.json())
	  .then(data => parseServerHello(data));
}

function doAsyncPredict() {
    Webcam.snap(function(data_uri) {
        fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'Authorization': 'Bearer ' + token
            },
            body: new URLSearchParams({'image': data_uri})
    
        }).catch(error => console.log(error.message))
          .then(response => response.json())
          .then(data => parsePredictedMood(data));
    });
}

function doAsyncMoodSend(mood_value) {
    fetch ('/api/add_mood', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Bearer ' + token
        },
        body: new URLSearchParams({'token': token, 'mood_id': mood_value})
    }).then(response => response.json())
      .then(data => showMoodTaken(mood_value));
}

function doAsyncNoteSend(title, value) {
    fetch ('/api/add_note', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Bearer ' + token
        },
        body: new URLSearchParams({'token': token, 'title': title, 'note': value})
    }).then(response => response.json())
      .then(data => console.log(data));
}

function doAsyncNotesRequest() {
    fetch ('/api/get_notes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Bearer ' + token
        },
        body: new URLSearchParams({'token': token})
    }).then(response => response.json())
      .then(data => processNotes(data));
}

function doAsyncRequestMoods(period, callback) {
    fetch ('/api/get_moods', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Bearer ' + token
        },
        body: new URLSearchParams({'token': token, 'timeperiod': period})
    }).then(response => response.json())
      .then(data => callback(data));
}

function doAsyncVisitSend(date, note) {
    fetch ('/api/add_visit', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Bearer ' + token
        },
        body: new URLSearchParams({'token': token, 'date': date, 'title': note})
    }).then(response => response.json())
      .then(data => console.log(data));
}

function doAsyncRequestVisits(callback) {
    fetch ('/api/get_visits', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Bearer ' + token
        },
        body: new URLSearchParams({'token': token})
    }).then(response => response.json())
      .then(data => callback(data));
}

function doAsyncCheckUpcomingVisit(callback) {
    fetch ('/api/has_upcoming_visit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Authorization': 'Bearer ' + token
        },
        body: new URLSearchParams({'token': token})
    }).then(response => response.json())
      .then(data => callback(data));
}

window.apiReady = true;
