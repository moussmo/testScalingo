from flask import Flask, render_template, request,redirect,url_for
import os
import requests
import json

import database.models
from config.config import Config
from database.init import db,init_database

api_key = "76492f1cc7209a0e7210f0f223555b6f"

port = os.getenv("PORT")
app = Flask(__name__)
route_accueil="/"
route_weather="/weather"

app.config.from_object(Config)
db.init_app(app)

with app.test_request_context():
    init_database()

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html', route_accueil=route_accueil,route_weather=route_weather)

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
        return render_template('weather.html',resultat = "A " + city +", Température min : " + str(int(temp_min)) + "°C ; Température max : " + str(int(temp_max)) +"°C" )
    #return json.dumps({'temperature':(temp_min + temp_max) / 2})
    else:
        return render_template('weather.html',resultat = "", route_accueil=route_accueil,route_weather=route_weather)

@app.route('/calendar', methods=['GET'])
def calendar():
    return render_template('calendar.html',resultat = "", route_accueil=route_accueil,route_weather=route_weather)

@app.route('/user/<username>', methods=['GET'])
def user(username=None):
    user=database.models.User()
    user.username=username
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/users', methods=['GET'])
def users():
    users=database.models.User.query.order_by(database.models.User.id.desc()).all()
    result=""
    for user in users:
        result+=user.username
    return render_template('index.html',result=result)

if __name__ == '__main__':
    print("Webhook démarré")
    app.run(host='0.0.0.0', port=port)