from app import db
from datetime import datetime

class DiseaseInfo(db.Model):
    __tablename__ = 'disease_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable = False)
    description = db.Column(db.Text)
    possible_steps = db.Column(db.Text)


    def __init__(self, name, description, possible_steps):
        self.name = name
        self.description = description
        self.possible_steps = possible_steps

    def __repr__(self):
        return f'<disease_info {self.id}>'