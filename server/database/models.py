from tkinter.tix import DECREASING
from flask_login import UserMixin
from database.init import db

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    #TODO: student id (authentification)
    student = db.Column(db.String(32))
    year = db.Column(db.Integer)

def add_internship(internship):
    print("Add")
    db.session.add(internship)
    db.session.commit()

def get_internship_by_id(internship_id):
    return Internship.query.filter_by(id=internship_id).first()

def get_internships_by_student(student_id):
    return Internship.query.filter_by(student=student_id).order_by(Internship.id.desc())

def get_internships_by_student_and_year(student_name, internship_year):
    return Internship.query.filter_by(student=student_name).filter_by(year=internship_year)

def remove_internship(internship_id):
    db.session.delete(Internship.query.filter_by(id=internship_id))
    db.session.commit()

class Event(db.Model):
    __tablename__ = 'events'
    #TODO
    #Doit prendre en compte un nombre de participants, un orga,...
    #Un projet (evenement fise)
    #Un organisme (Taf)
    #Une salle
    #Alertes, périodicité..
    #Catégories (séminaire...)

    id = db.Column(db.Integer, primary_key=True,unique=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    #created_date = db_alchemy.Column(db_alchemy.DateTime, nullable=False)
    #last_modified_date = db_alchemy.Column(db_alchemy.DateTime, nullable=False)
    #event_owner = db_alchemy.Column(db_alchemy.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    #details = db.Column(db.Text(1000))

    participants = db.Column(db.String(10000)) #format : <id_user_1>;<id_user_2>;...;<id_user_n>

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    events = db.Column(db.String(10000)) #format : <id_event_1>;<id_event_2>;...;<id_event_n>
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def get_id(self):
        return self.user_id

