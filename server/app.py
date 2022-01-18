from flask import Flask, render_template, request,redirect,url_for, jsonify, flash
import os
import requests
import json
import datetime

from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash


import utils
import database.models
from config.config import Config
from database.init import db, init_database
from database.models import User

api_key = "76492f1cc7209a0e7210f0f223555b6f"

port = os.getenv("PORT")
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

route_accueil="/"
route_weather="/weather"
route_calendar="/calendar"
route_users="/users"

with app.test_request_context():
    init_database()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    disconnected = bool(request.args.get('disconnected'))
    if disconnected is True:
        flash('Vous vous êtes déconnecté avec succès.')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Vérifiez vos identifiants et réessayez.')
        return redirect(url_for('login'))

    login_user(user, remember=remember)
    return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login', disconnected=True))

@app.route('/calendar', methods=['GET'])
def calendar():
    user = database.models.User.query.filter_by(user_id=1).first()
    print(user)
    print(user.events)
    events_id = user.events.split(";")
    events=[]
    for event_id in events_id:
        event = database.models.Event.query.filter_by(id=event_id).first()
        #start_date = event.
        events.append(event.as_dict())
    return render_template('calendar.html',resultat = "", #events=str(events), 
    route_accueil=route_accueil,
    route_weather=route_weather,
    route_calendar=route_calendar,
    route_users=route_users)

@app.route('/post_events',methods=['POST'])
def post_events():
    form = request.form
    user_id = form["user_id"]
    user = database.models.User.query.filter_by(user_id=user_id).first()
    print(user)
    print(user.events)
    events_id = user.events.split(";")
    events=[]
    for event_id in events_id:
        event = database.models.Event.query.filter_by(id=event_id).first()
        events.append(event.as_dict())
    print(user_id)
    print(events)
    return jsonify(events)

@app.route('/calendar/event',methods=['GET','POST'])
@app.route('/calendar/event/<id>',methods=['GET','POST'])
def event(id=None):
    #Datetime doc : https://www.w3schools.com/python/python_datetime.asp
    event = database.models.Event.query.filter_by(id=id).first()
    users = database.models.User.query.all()
    form = request.form
    errors=[]
    #errors=["broo"]
    if request.method=='POST':
        if not event:
            event = database.models.Event()
        title= form.get("title_event")
        debut_heure= int(form.get("start_hour"))
        debut_min= int(form.get("start_min"))
        fin_heure= int(form.get("end_hour"))
        fin_min= int(form.get("end_min"))
        date_str=form.get("date")
        date_d,date_m,date_y=utils.parse_date(date_str)
        participants_id=str(form.get("participants_id_name"))


        event.title=title
        event.start=datetime.datetime(date_y,date_m,date_d,debut_heure,debut_min)
        event.end=datetime.datetime(date_y,date_m,date_d,fin_heure,fin_min)
        if participants_id!="":
            ids = participants_id.split(";")
            if event.participants:
                for id in ids:
                    if id not in event.participants.split(";"):
                        event.participants = event.participants + ";" + str(id)
            else:
                event.participants=participants_id
        print("event.participants : " + str(event.participants))
        
        if len(errors)==0:
            db.session.add(event)
            db.session.commit()

            for participant_id in participants_id.split(";"):
                participant = database.models.User.query.filter_by(user_id=participant_id).first()
                print("participant.name : " + participant.name)
                print("event.id : " + str(event.id))
                result=participant.events
                if result:
                    ids = participant.events.split(";")
                    print("ids in participant commit : " +str(ids))
                    if not event.id in ids:
                        result = result + ";" + str(event.id)
                else:
                    result = str(event.id)
                participant.events=result
                print("result : " +result)
                db.session.add(participant)
                db.session.commit()

            return redirect(url_for('calendar'))
        else:
            return render_template('event.html',resultat = "", errors=errors, users=users,
            route_accueil=route_accueil,
            route_weather=route_weather,
            route_calendar=route_calendar,
            route_users=route_users)
    else:
        return render_template('event.html',resultat = "", users=users, 
            route_accueil=route_accueil,
            route_weather=route_weather,
            route_calendar=route_calendar,
            route_users=route_users)

@app.route('/calendar/events', methods=['GET'])
def list_events():
    events = database.models.Event.query.all()
    result = ""
    for event in events:
        result+= event.title
    return render_template('index.html',result=result, 
    route_accueil=route_accueil,
    route_weather=route_weather,
    route_calendar=route_calendar,
    route_users=route_users)

@app.route('/user/<name>', methods=['GET'])
def user(name=None):
    user=database.models.User()
    user.name=name
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/users', methods=['GET'])
def users():
    users=database.models.User.query.order_by(database.models.User.user_id.desc()).all()
    result=""
    for user in users:
        result+=user.name + str(user.user_id)
    return render_template('index.html',result=result, 
    route_accueil=route_accueil,
    route_weather=route_weather,
    route_calendar=route_calendar,
    route_users=route_users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)