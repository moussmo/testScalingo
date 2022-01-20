from sys import intern
from flask import Flask, render_template, request,redirect,url_for, jsonify, flash
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests
import json
import datetime

import utils

from config.config import Config
from database.models import User
from database.init import db, init_database
from database.models import *
from database.init import db,init_database

import extension_build
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request,redirect,url_for, jsonify, flash
from flask_login import login_user, logout_user, login_required, LoginManager, current_user

port = os.getenv("PORT")
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

route_accueil="/"
route_weather="/weather"
route_calendar="/calendar"
route_users="/users"
route_internships="/internships"

with app.test_request_context():
    init_database()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
  
@app.route('/',methods=['GET'])
@login_required
def index():
    return render_template('index.html', 
    route_accueil=route_accueil,
    route_weather=route_weather,
    route_calendar=route_calendar,
    route_users=route_users,
    route_internships=route_internships)

@app.route('/base_extension')
def index_extension():
    return render_template('/base_extensions.html')

@app.route('/login')
def login():
    disconnected = bool(request.args.get('disconnected'))
    unsubscribed = bool(request.args.get('unsubscribed'))
    already_connected = bool(request.args.get('already_connected'))
    if already_connected is True:
        return redirect(url_for('index'))
        #flash('Vous êtes déjà connecté.')
    if unsubscribed is True:
        flash('Compte supprimé avec succès.')
    if disconnected is True:
        flash('Vous vous êtes déconnecté avec succès.')
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    if current_user.get_id() is not None:
        return redirect(url_for('login', already_connected=True))

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Vérifiez vos identifiants et réessayez.')
        return redirect(url_for('login'))

    login_user(user, remember=remember)
    return redirect(url_for('index'))


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

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), events="")

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login', disconnected=True))

@app.route('/unsubscribe', methods=['POST'])
@login_required
def unsubscribe():
    current_user_id = current_user.user_id
    logout_user()
    User.query.filter_by(user_id=current_user_id).delete()
    db.session.commit()
    return redirect(url_for('login', unsubscribed=True))

  
@app.route('/extension/<name>')
def extension_route(name):
    return render_template('extension_{}.html'.format(name))
  
  
@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    user = current_user
    extension = bool(request.form.get('extension'))
    if extension == True:
        html_page = 'calendar_extension.html'
    else:
        html_page = 'calendar.html'

    return render_template(html_page, resultat = "", #events=str(events),
    route_accueil=route_accueil,
    route_weather=route_weather,
    route_calendar=route_calendar,
    route_users=route_users)


@app.route('/post_events',methods=['POST'])
@login_required
def post_events():
    form = request.form
    #user_id = form["user_id"]
    user = current_user
    print(user)
    print(user.name)
    print(user.events)
    if user.events!="":
        events_id = user.events.split(";")
        events=[]
        for event_id in events_id:
            event = Event.query.filter_by(id=event_id).first()
            events.append(event.as_dict())
    else:
        events=[]
    print(events)
    return jsonify(events)


@app.route('/calendar/event',methods=['GET','POST'])
@app.route('/calendar/event/<id>',methods=['GET','POST'])
@login_required
def event(id=None):
    #Datetime doc : https://www.w3schools.com/python/python_datetime.asp
    print(id)
    event = Event.query.filter_by(id=id).first()
    print(event)
    users = User.query.all()
    form = request.form
    errors=[]
    #errors=["broo"]
    if request.method=='POST':
        if event is None:
            event = Event()
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
                participant = User.query.filter_by(user_id=participant_id).first()
                print("participant.name : " + participant.name)
                print("event.id : " + str(event.id))
                result=participant.events
                if result:
                    ids = participant.events.split(";")
                    print("ids in participant commit : " +str(ids))
                    if id!=None:
                        result = result + ";" + str(event.id)
                else:
                    result = str(event.id)
                participant.events=result
                print("result : " +result)
                db.session.add(participant)
                db.session.commit()

            return redirect(url_for('calendar'))
        else:
            return render_template('event.html',resultat = "", errors=errors, users=users, id=id,
            route_accueil=route_accueil,
            route_weather=route_weather,
            route_calendar=route_calendar,
            route_users=route_users)
    else:
        return render_template('event.html',resultat = "", users=users, id=id,
            route_accueil=route_accueil,
            route_weather=route_weather,
            route_calendar=route_calendar,
            route_users=route_users)

@app.route('/calendar/events', methods=['GET'])
def list_events():
    events = Event.query.all()
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
    user=User()
    user.name=name
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/users', methods=['GET'])
def users():
    users=User.query.order_by(User.user_id.desc()).all()
    result=""
    for user in users:
        result+=user.name + str(user.user_id)
    return render_template('index.html',result=result, 
    route_accueil=route_accueil,
    route_weather=route_weather,
    route_calendar=route_calendar,
    route_users=route_users)

@app.route('/internships', methods=["GET", 'POST'])
@login_required
def internships_main():
    internships=get_internships_by_student(current_user.user_id)
    user=get_user_by_id(current_user.user_id)
    extension = bool(request.form.get('extension'))
    if extension == True:
        html_page = 'internships_main_extension.html'
    else:
        html_page = 'internships_main.html'

    return render_template(html_page, results=internships, student=user)

@app.route('/internships/new', methods=["GET", "POST"])
@app.route('/internships/new/<id>', methods=["GET", "POST"])
def internship_form(id=None):
    internship = get_internship_by_id(id)
    form = request.form
    if (request.method == 'POST'):
        extension = bool(request.form.get('extension'))
        if extension == True:
            return render_template('internships_form_extension.html', intern=internship)
        if internship is None:
            internship = Internship()
        internship.title = form.get("title", "")
        internship.agreement_title=form.get("agreement_title", "")
        internship.description=form.get("description", "")
        internship.mission=form.get("mission", "")
        internship.staff=form.get("staff", "")
        internship.research_argument=form.get("research_argument", "")
        internship.date_beginning=form.get("date_beginning", "")
        internship.date_end=form.get("date_end", "")
        internship.hours_per_week=form.get("hours_per_week", "")
        internship.schedule=form.get("schedule", "")
        internship.language=form.get("language", "")
        internship.year = form.get("year", "")
        internship.campus=form.get("campus", "")
        internship.option=form.get("option", "")

        internship.company_name=form.get("company_name", "")
        internship.company_group=form.get("company_group", "")
        print(internship.company_name)
        if (internship.company_name != ""):
            internship.company_siret=search_siret(internship.company_name)
        internship.company_phone=form.get("company_phone", "")
        internship.company_adress=form.get("company_adress", "")
        internship.company_postal_code=form.get("company_postal_code", "")
        internship.company_city=form.get("company_city", "")
        internship.company_country=form.get("company_country", "")

        internship.tutor_civility=form.get("tutor_civility", "")
        internship.tutor_name=form.get("tutor_name", "")
        internship.tutor_surname=form.get("tutor_surname", "")
        internship.tutor_job=form.get("tutor_job", "")
        internship.tutor_email=form.get("tutor_email", "")
        internship.tutor_phone=form.get("tutor_phone", "")

        internship.student_id = current_user.user_id
        internship.date=datetime.datetime.now()
        add_internship(internship)
        return redirect(url_for('internships_main'))

    return render_template('internships_form.html', intern=internship)

def search_siret(name):
    name = name.upper()
    today = datetime.datetime.now()
    now = today.strftime("%Y-%m-%d")
    url = 'https://api.insee.fr/entreprises/sirene/V3/siret?q=denominationUniteLegale%3A'+ name+ '&date=' + now
    print("url", url)
    key = 'Bearer 9d62e645-03c2-35c5-8fe3-f7a51cf31a9c'
    headers = {'Accept': 'application/json', 'Authorization': key}
    result = requests.get(url, headers=headers).json()
    siret=result["etablissements"][0]["siret"]
    return(siret)

@app.route('/internships/delete/<id>', methods=["GET"])
def delete_internship(id=None):
    remove_internship(id)
    return redirect(url_for('internships_main'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)