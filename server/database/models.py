from flask_login import UserMixin
from database.init import db




class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    events = db.Column(db.String(10000)) #format : <id_event_1>;<id_event_2>;...;<id_event_n>
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def get_id(self):
        return self.user_id

class Event(db.Model):
    __tablename__ = 'event'
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

    room = db.Column(db.String(100))
    organisateur_id = db.Column(db.Integer)
    #created_date = db_alchemy.Column(db_alchemy.DateTime, nullable=False)
    #last_modified_date = db_alchemy.Column(db_alchemy.DateTime, nullable=False)
    owner_id = db.Column(db.Integer)
    title = db.Column(db.String(50), nullable=False)
    #details = db.Column(db.Text(1000))

    participants = db.Column(db.String(10000)) #format : <id_user_1>;<id_user_2>;...;<id_user_n>

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
