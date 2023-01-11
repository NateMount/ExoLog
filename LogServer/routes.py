#! /usr/bin/env python3.9
#  App Routes File

from yaml import load
from os import path
from flask import render_template, Markup, redirect, url_for, session, request, jsonify
from flask_login import login_required, login_user, current_user

from LogServer import app
from LogServer.db_broker import UserBroker
from LogServer.forms import LoginForm, RegistrationForm, RegistrationForm



@app.route("/")
def index(): 
    return render_template("core.html", 
        title="ExoLog", 
        desc="Remote logging soultions", 
        url="https://ExoLog.io/", 
        style="index", 
        content=Markup(render_template('index.html'))
    )

@app.route("/plans")
def plans(): 
    return render_template('core.html',
        title='Plans',
        desc='ExoLog hosting payment plans',
        url='https://ExoLog.io/plans',
        style='plans',
        content=Markup(render_template('plans.html'))
    )

@app.route("/register", methods=["GET", "POST"])
def register():
        if (form := RegistrationForm()).validate_on_submit():
            if (username := form.username.data) in [ u.name for u in UserBroker.get_users()]: 
                # session['data'] = ""
                return render_template('register.html', form=form, errors=True)
            else:
                UserBroker.new(username=username, password=form.passwd.data)
                # session['data'] = username
                return redirect(url_for("home"))

        return render_template('register.html', form=form, errors=False, name="" if 'data' not in session else session['data'])

@app.route("/login", methods=["GET", "POST"])
def login(): 
    session['data'] = ""
    if (form := LoginForm()).validate_on_submit():
        if (username := form.username.data) in [ u.name for u in UserBroker.get_users()]:
            if UserBroker.authenticate(username=username, password=form.passwd.data):
                login_user(UserBroker.get_users(name=username)[0],remember=True)
                return redirect(url_for("home"))
        else:
            # if username: session['data'] = username
            return redirect(url_for("register"))

    return render_template('login.html', form=form)

@app.route("/info")
def info(): 
    return render_template("core.html",
        title="ExoLog | More Info",
        desc="ExoLog Info Page",
        url="https://ExoLog.io/info",
        style="info",
        content=Markup(render_template('info.html'))
    )

@app.route("/libraries")
def libraries(): 
    return render_template("core.html",
        title="ExoLog Libraries",
        desc="ExoLog API Libraries",
        url="https://ExoLog.io/libraries",
        style="lib",
        content=Markup(render_template('lib.html', tileset=load(open(path.join(app.static_folder, 'persistance/langs.yaml')))))
    )

@app.route("/home")
@login_required
def home(): 
    return render_template('user_wrapper.html', 
        name=current_user.name,
        content=Markup(render_template('analytics.html'))
    )

@app.errorhandler(404)
def not_found(e):
    if request.method == 'GET':
        return render_template("core.html",
            title="404",
            desc="Page not found",
            url="https://ExoLog.io/",
            style="error",
            content=Markup("<h1 style=\"font-family: 'aquire'; font-size: 180px; width:100%; text-align: center; margin-top: 20%; height: 60%\" class=\"noselect\">404</h1>")
        ), 404
    else: return jsonify({'errorCode': 404, 'message': 'Page not found'})

@app.errorhandler(500)
def server_error(e):
    if request.method in ('GET', 'POST'):
        return render_template("core.html",
            title="Server Error",
            desc="Internal Server Error",
            url="https://ExoLog.io/",
            style="error",
            content=Markup("<h1 style=\"font-family: 'aquire'; font-size: 180px; width:100%; text-align: center; margin-top: 20%; height: 60%\" class=\"noselect\">Internal Server Error</h1>")
        ), 500
    else: return jsonify({'errorCode': 500, 'message': 'Server Error'}), 500