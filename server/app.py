from flask import Flask, render_template, request,redirect,url_for, jsonify
import os
import requests
import json
import datetime

import utils
import database.models
from config.config import Config
from database.init import db,init_database

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

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html', 
    route_accueil=route_accueil,
    route_weather=route_weather,
    route_calendar=route_calendar,
    route_users=route_users)

@app.route('/weather', methods=['GET','POST'])
def weather():
    if request.method=="POST":
        city = request.form.get('city')
        url = "http://api.openweathermap.org/data/2.5/weather/?q=" + city + "&lang=fr&APPID=" + api_key
        print("appel de l'url :" + url)
        r = requests.get(url)
        resultat = r.json()
        temp_min = resultat['main']['temp_min'] - 273.15
        temp_max = resultat['main']['temp_max'] - 273.15
        return render_template('weather.html',resultat = "A " + city +", Température min : " + str(int(temp_min)) + "°C ; Température max : " + str(int(temp_max)) +"°C" , 
            route_accueil=route_accueil,
            route_weather=route_weather,
            route_calendar=route_calendar,
            route_users=route_users)
    #return json.dumps({'temperature':(temp_min + temp_max) / 2})
    else:
        return render_template('weather.html',resultat = "", 
        route_accueil=route_accueil,
        route_weather=route_weather,
        route_calendar=route_calendar,
        route_users=route_users)

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
                print("participant.username : " + participant.username)
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

@app.route('/user/<username>', methods=['GET'])
def user(username=None):
    user=database.models.User()
    user.username=username
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/users', methods=['GET'])
def users():
    users=database.models.User.query.order_by(database.models.User.user_id.desc()).all()
    result=""
    for user in users:
        result+=user.username + str(user.user_id)
    return render_template('index.html',result=result, 
    route_accueil=route_accueil,
    route_weather=route_weather,
    route_calendar=route_calendar,
    route_users=route_users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)