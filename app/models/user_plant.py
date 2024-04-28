import datetime
from app import db
from sqlalchemy.sql import func

class UserPlant(db.Model):
    __tablename__ = 'user_plant'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    user_image_url = db.Column(db.String(200))
    last_watered = db.Column(db.DateTime, server_default = func.now())
    notes = db.Column(db.Text)
    current_disease = db.Column(db.Integer, db.ForeignKey('disease_info.id'), nullable=False)
    date_added = db.Column(db.DateTime, server_default = func.now())

    def __init__(self, user_id, plant_id, last_watered, notes, current_disease):
        self.user_id=user_id
        self.plant_id = plant_id
        self.last_watered = last_watered
        self.notes = notes
        self.current_disease = current_disease

    def __repr__(self):
        return f'<Profile of User {self.user.username}>'