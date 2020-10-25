from flask import Flask, Blueprint, request, render_template, session, redirect, url_for

INTERFACE_ROUTE = "/"
interface = Blueprint('interface', __name__, template_folder='templates', static_folder='assets')

@interface.route(INTERFACE_ROUTE)
def interface_index():
	if ("token" in session):
		return render_template("index.html")
	else:
		return redirect(url_for('interface.interface_login'))

@interface.route(INTERFACE_ROUTE + "notes")
def interface_notes():
        if ("token" in session):
                return render_template("notes.html")
        else:
                return redirect(url_for('interface.interface_login'))

@interface.route(INTERFACE_ROUTE + "charts")
def interface_charts():
        if ("token" in session):
                return render_template("charts.html")
        else:
                return redirect(url_for('interface.interface_login'))

@interface.route(INTERFACE_ROUTE + "visits")
def interface_visits():
        if ("token" in session):
                return render_template("visits.html")
        else:
                return redirect(url_for('interface.interface_login'))

@interface.route(INTERFACE_ROUTE + "login")
def interface_login():
	return render_template("login.html")

@interface.route(INTERFACE_ROUTE + "register")
def interface_register():
	return render_template("register.html")
