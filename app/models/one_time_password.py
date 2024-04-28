from datetime import datetime
import random
from app import db
from sqlalchemy.sql import func

class OneTimePassword(db.Model):
    __tablename__ = 'one_time_password'
    id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, server_default = func.now())
    otp_code = db.Column(db.Integer, default = random.randint(100000,999999))

    def __init__(self, user_email):
        self.user_email = user_email
        self.timestamp = datetime.utcnow()
        self.otp_code = random.randint(100000,999999)

    def __repr__(self):
        return f'<OTP Code {self.otp_code} Generated for {self.user_email} at {self.timestamp}>'