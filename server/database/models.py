from tkinter.tix import DECREASING
from flask_login import UserMixin
from database.init import db

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date=db.Column(db.DateTime)
    student_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    #company
    company_name=db.Column(db.String(64))
    company_group=db.Column(db.String(64))
    company_siret=db.Column(db.String(64))
    company_phone=db.Column(db.String(64))
    company_adress=db.Column(db.String(256))
    company_postal_code=db.Column(db.String(32))
    company_city=db.Column(db.String(64))
    company_country=db.Column(db.String(64))
    #description
    title = db.Column(db.String(128))
    agreement_title=db.Column(db.String(128))
    description=db.Column(db.String(256))
    mission=db.Column(db.String(256))
    staff=db.Column(db.String(32))
    research_argument=db.Column(db.String(256))
    #TODO fix dates
    date_beginning=db.Column(db.String(64))
    date_end=db.Column(db.String(64))
    hours_per_week=db.Column(db.String(64))
    schedule=db.Column(db.String(256))
    #TODO fix choice options
    language=db.Column(db.String(64))
    campus=db.Column(db.String(64))
    year = db.Column(db.Integer)
    option=db.Column(db.String(64))
    #tutor
    tutor_civility=db.Column(db.String(64))
    tutor_name=db.Column(db.String(64))
    tutor_surname=db.Column(db.String(64))
    tutor_job=db.Column(db.String(128))
    tutor_email=db.Column(db.String(64))
    tutor_phone=db.Column(db.String(64))
    #TODO: find a way to deal with attachments

def add_internship(internship):
    print("Add")
    db.session.add(internship)
    db.session.commit()

def get_internship_by_id(internship_id):
    return Internship.query.filter_by(id=internship_id).first()

def get_internships_by_student(student):
    print(student)
    return Internship.query.filter_by(student_id=student).order_by(Internship.id.desc())

def get_internships_by_student_and_year(student_id, internship_year):
    return Internship.query.filter_by(student_id=student_id).filter_by(year=internship_year)

def remove_internship(internship_id):
    db.session.delete(Internship.query.filter_by(id=internship_id).first())
    db.session.commit()

def get_user_by_id(user_id):
    return User.query.filter_by(user_id=user_id).first()

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

