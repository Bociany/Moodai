from flask import Flask, Blueprint, request, session
from flask_httpauth import HTTPTokenAuth
from sqlalchemy import desc

from auth import verify_token, generate_token, token_exists, hash_multiple, remove_token
from database import *
from models.user import User
from models.mood import Mood
from models.notes import Notes
import tensorflow_predictor

import dateutil.parser
import hashlib
import datetime
import urllib
import tempfile
import cv2
import uuid
import json

API_ROUTE = "/api/"
api = Blueprint('api', __name__)
auth = HTTPTokenAuth(scheme='Bearer')

# HTTPTokenAuth passthrough, calls verify_token from auth.py
@auth.verify_token
def AUTH_verify_token(token):
	return verify_token(token)

# Verifies the token server-side, will return either true or false
@api.route(API_ROUTE + "verify_token", methods=["POST"])
def API_verify_token():
	return json.dumps({"active": token_exists(request.form["token"])})

# Predicts the given image
# Takes in a data uri encoded image and passes it through to tensorflow_predictor.py
@api.route(API_ROUTE + "predict", methods=["POST"])
@auth.login_required
def API_predict_image():
	# The image is stored as a data/uri component, we need to extract it and temporarily save it
	image_resp = urllib.request.urlopen(request.form["image"])
	filepath = tempfile.gettempdir() + "/" + str(uuid.uuid4()) + ".png"

	with open(filepath, "wb") as temp_image:
		temp_image.write(image_resp.file.read())
		print("api: predict wrote temporary file to " + filepath)

	# Ask the tensorflow predictor to get us the max coefficients for the image
	# TODO: Convert them to a string representation later on and send this as json
	return json.dumps({"mood_value": tensorflow_predictor.get_max_idx_from_image(cv2.imread(filepath))})

@api.route(API_ROUTE + "login", methods=["POST"])
def API_login():
	# Check if the email exists
	users = get_session().query(User).filter_by(email=request.form["email"]).all()
	if (len(users) < 1):
		return json.dumps({"state": "error", "message": "Invalid e-mail or password."})

	our_user = users[0]
	# Check if the password supplied is the same as the password in the User model
	if (our_user.password != hash_multiple([request.form["email"], request.form["password"]])):
		return json.dumps({"state": "error", "message": "Invalid e-mail or password."})

	session['token'] = generate_token(our_user.id)
	return json.dumps({"state": "ok", "message": "", "token": session['token']})


@api.route(API_ROUTE + "register", methods=["POST"])
def API_register():
	# Check if the email already exists
	if (len(get_session().query(User).filter_by(email=request.form["email"]).all()) > 0):
		return json.dumps({"state": "error", "message": "E-mail already registered!"})

	password = hash_multiple([request.form["email"], request.form["password"]])
	user = User(email=request.form["email"], fullname=request.form["fullname"], password=password)
	push_model(user)

	# Get back the users, I shouldn't do it like this
	db_users = get_session().query(User).filter_by(email=request.form["email"]).all()
	session['token'] = generate_token(db_users[0].id)
	return json.dumps({"state": "ok", "message": "", "token": session['token']})


@auth.login_required
@api.route(API_ROUTE + "logout", methods=["POST"])
def API_logout():
	user_id = verify_token(request.form["token"])
	if (user_id is None):
		return json.dumps({"state": "error", "message": "Invalid token"})

	remove_token(request.form["token"])
	session.pop('token', None)

	return json.dumps({"state": "ok", "message": ""})

@auth.login_required
@api.route(API_ROUTE + "hello", methods=["POST"])
def API_hello():
	user_id = int(verify_token(request.form["token"]))
	print ("api: hello->user_id is: " + str(user_id))
	should_mood_update = False
	mood_value = None
	moods = []

	has_upcoming_visit = False
	upcoming_visit_date = None

	user = get_session().query(User).filter_by(id=user_id).all()[0]

	try:
		# TODO: Make this line shorter
		latest_seven_moods = get_session().query(Mood).filter_by(user_id=user_id).order_by(desc(Mood.created_at)).limit(7).all()
		latest_mood = latest_seven_moods[0]

		if latest_mood.created_at < datetime.datetime.now() - datetime.timedelta(hours=24):
			should_mood_update = True

		for mood in latest_seven_moods:
			moods.append({"value": mood.mood, "time": mood.created_at.isoformat()})

		mood_value = latest_mood.mood

		next_visits = get_session().query(Visit).filter_by(user_id=user_id).order_by(desc(Visit.scheduled_for)).limit(1).all()

		if len(next_visits) > 0:
			next_visit = next_visits[0]
			if next_visit.scheduled_for > datetime.datetime.now() - datetime.timedelta(hours=24):
				has_upcoming_visit = True
				upcoming_visit_date = next_visit.scheduled_for.isoformat()
	except Exception as inst:
		should_mood_update = True
		print ("api: Error happened in /api/hello - " + str(inst))

	avatar_hash = hashlib.md5(user.email.encode())

	return json.dumps({"update_mood": should_mood_update, "latest_mood_value": mood_value, "moods": moods, "fullname": user.fullname, "avatar_hash": avatar_hash.hexdigest(), "has_upcoming_visit": has_upcoming_visit, "next_upcoming_visit": upcoming_visit_date})

@auth.login_required
@api.route(API_ROUTE + "add_mood", methods=["PUT"])
def API_add_mood():
	user_id = int(verify_token(request.form["token"]))

	mood = Mood(user_id=user_id, mood=request.form["mood_id"])
	push_model(mood)
	return json.dumps({"state": "ok"})

@auth.login_required
@api.route(API_ROUTE + "add_note", methods=["PUT"])
def API_add_note():
        user_id = int(verify_token(request.form["token"]))

        note = Notes(user_id=user_id, title=request.form['title'], note=request.form["note"])
        push_model(note)
        return json.dumps({"state": "ok"})

@auth.login_required
@api.route(API_ROUTE + "get_notes", methods=["POST"])
def API_get_notes():
        user_id = int(verify_token(request.form["token"]))

        notes = []
        notes_iterator = get_session().query(Notes).filter_by(user_id=user_id).all()
        for note in notes_iterator:
                notes.append({"title": note.title, "message": note.note})
        return json.dumps({"state": "ok", "notes": notes})


@auth.login_required
@api.route(API_ROUTE + "get_moods", methods=["POST"])
def API_get_moods():
	user_id = int(verify_token(request.form["token"]))
	moods = []

	latest_moods = get_session().query(Mood).filter_by(user_id=user_id).order_by(desc(Mood.created_at)).limit(int(request.form["timeperiod"])).all()
	for mood in latest_moods:
		moods.append({"value": mood.mood, "time": mood.created_at.isoformat()})


	return json.dumps({"state": "ok", "moods": moods})

@auth.login_required
@api.route(API_ROUTE + "add_visit", methods=["PUT"])
def API_add_visit():
	user_id = int(verify_token(request.form["token"]))

	visit = Visit(scheduled_for=dateutil.parser.parse(request.form["date"]), note=request.form["title"], user_id=user_id)
	push_model(visit)

	return json.dumps({"state": "ok"})

@auth.login_required
@api.route(API_ROUTE + "get_visits", methods=["POST"])
def API_get_visits():
        user_id = int(verify_token(request.form["token"]))

        visits = []
        visits_iterator = get_session().query(Visit).filter_by(user_id=user_id).all()
        for visit in visits_iterator:
                visits.append({"date": visit.scheduled_for.isoformat(), "note": visit.note})
        return json.dumps({"state": "ok", "visits": visits})


@auth.login_required
@api.route(API_ROUTE + "has_upcoming_visit", methods=["POST"])
def API_has_upcoming_visit():
	user_id = int(verify_token(request.form["token"]))
	has_upcoming_visit = False
	upcoming_visit_date = None

	next_visits = get_session().query(Visit).filter_by(user_id=user_id).order_by(desc(Visit.scheduled_for)).limit(1).all()

	if len(next_visits) > 0:
		next_visit = next_visits[0]
		if next_visit.scheduled_for > datetime.datetime.now() - datetime.timedelta(hours=24):
			has_upcoming_visit = True
			upcoming_visit_date = next_visit.scheduled_for.isoformat()

	return json.dumps({"state": "ok", "has_upcoming_visit": has_upcoming_visit, "next_upcoming_visit": upcoming_visit_date})
