import datetime
from app import db
from sqlalchemy.sql import func

class PasswordHistory(db.Model):
    __tablename__ = 'password_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, server_default = func.now())

    def __init__(self, user_id, password_hash,timestamp):
        self.user_id = user_id
        self.password_hash = password_hash
        self.timestamp = timestamp

    def __repr__(self):
        return f'<PasswordHistory for User {self.user_id} at {self.timestamp}>'