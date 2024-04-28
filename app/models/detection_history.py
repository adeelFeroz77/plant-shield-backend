from app import db
from datetime import datetime
from sqlalchemy.sql import func

class DetectionHistory(db.Model):
    __tablename__ = 'detection_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    user_plant_id = db.Column(db.Integer, db.ForeignKey('user_plant.id'), nullable=False)
    detected_disease = db.Column(db.Integer, db.ForeignKey('disease_info.id'), nullable=False)
    is_accurate_prediction = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, server_default = func.now())


    def __init__(self, user_id, plant_id,user_plant_id, detected_disease, is_accurate_prediction, timestamp):
        self.user_id = user_id
        self.plant_id = plant_id
        self.user_plant_id = user_plant_id
        self.detected_disease = detected_disease
        self.is_accurate_prediction = is_accurate_prediction
        self.timestamp = datetime.utcnow() if timestamp is None else timestamp

    def __repr__(self):
        return f'<detection_history {self.id}>'