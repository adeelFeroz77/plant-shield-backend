import datetime
from app import db

class UserPlant(db.Model):
    __tablename__ = 'user_plant'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    user_image_url = db.Column(db.String(200))
    last_watered = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    current_disease = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, fullname, bio, gender, phone,user_id):
        self.fullname = fullname
        self.bio = bio
        self.gender = gender
        self.phone = phone
        self.user_id=user_id

    def __repr__(self):
        return f'<Profile of User {self.user.username}>'