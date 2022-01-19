from sys import intern
from flask import Flask, render_template, request, redirect, url_for
import os
import requests
import json
from database.database import db, init_database

from database.models import *

api_key = "76492f1cc7209a0e7210f0f223555b6f"

port = os.getenv("PORT")
app = Flask(__name__)
db.init_app(app)
with app.test_request_context():
    init_database()
route_accueil="/"
route_weather="/weather"

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

@app.route('/internships', methods=["GET"])
def internships_main():
    internships=get_internships_by_student('Test')
    return render_template('internships_main.html', results=internships)

@app.route('/internships/new', methods=["GET", "POST"])
@app.route('/internships/new/<id>', methods=["GET", "POST"])
def internship_form(id=None):
    print("id:", id)
    internship = get_internship_by_id(id)
    if (request.method == 'POST'):
        if internship is None:
            internship = Internship()
        internship.title = request.form.get("title", "")
        internship.year = request.form.get("year", "")
        internship.student = "Test"
        add_internship(internship)
        return redirect(url_for('internships_main'))
    return render_template('internships_form.html', intern=internship)

if __name__ == '__main__':
    print("Webhook démarré")
    app.run(host='0.0.0.0', port=port)