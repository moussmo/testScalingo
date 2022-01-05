from flask import Flask
import os
import requests
import json

api_key = "76492f1cc7209a0e7210f0f223555b6f"

port = os.getenv("PORT")
app = Flask(__name__)

@app.route('/weather/<city>', methods=['GET'])
def weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather/?q=" + city + "&lang=fr&APPID=" + api_key
    print("appel de l'url :" + url)
    r = requests.get(url)
    resultat = r.json()
    temp_min = resultat['main']['temp_min'] - 273.15
    temp_max = resultat['main']['temp_max'] - 273.15
    return json.dumps({'temperature':(temp_min + temp_max) / 2})

if __name__ == '__main__':
    print("Webhook démarré")
    app.run(host='0.0.0.0', port=port)