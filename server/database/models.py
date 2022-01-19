from tkinter.tix import DECREASING
from database.database import db 

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
