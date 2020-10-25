var container = document.querySelector("#container");

doAsyncNotesRequest();

function addNote(title, value) {
	var note = document.createElement("div");
	note.id = "notatki";
	note.classList.add("karta-kolor");
	note.classList.add("karta");

	var titleElement = document.createElement("input");
	titleElement.value = title;
	titleElement.classList.add("note-area");
	titleElement.style.height = "50px";
	titleElement.disabled = true;

	var valueElement = document.createElement("textarea");
	valueElement.value = value;
	valueElement.classList.add("note-area");
	valueElement.disabled = true;

	note.appendChild(titleElement);
	note.appendChild(valueElement);

	container.appendChild(note);
}

function processNotes(data) {
	console.log(data);
	for (var i = 0; i < data.notes.length; i++) {
		var note = data.notes[i];
		addNote(note.title, note.message);
	}
}
