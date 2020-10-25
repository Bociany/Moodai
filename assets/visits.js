window.lastSelectedDate = null;
var pickerCalendarEl = document.querySelector('#picker-calendar');
var pickerCalendar = new FullCalendar.Calendar(pickerCalendarEl, {
    initialView: 'dayGridMonth',
    selectable: true,
    height: "100%",
    dateClick: function(info) {
        window.lastSelectedDate = info.dateStr;
    }
});

pickerCalendar.render();

doAsyncRequestVisits(function(data) {
    var calendarEl = document.querySelector('#kalendarz');
    var events = [];

    for (var i = 0; i < data.visits.length; i++) {
        var splitTime = data.visits[i].date.split('T');
        events.push({'id': splitTime, 'title': data.visits[i].note, 'start': splitTime[0]});
    }

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        height: 700,
        timeZone: 'UTC',
        events: events
    });

    calendar.render();
});

doAsyncCheckUpcomingVisit(function(data) {
    var visits = document.querySelector('.nadchodzaca-wizyta');

    if (data.has_upcoming_visit) {
        var splitDate = data.next_upcoming_visit.split('T');

        visits.innerHTML = "<h1>Twoja następna wizyta odbędzie się: " + splitDate[0] + ".</b>";
    }
});

function saveVisit() {
    var title = document.querySelector('#visit-title');
    doAsyncVisitSend(window.lastSelectedDate, title.value);

    title.value = "";
}