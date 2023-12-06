from app import db

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.String(500))
    gender = db.Column(db.String(6))
    phone = db.Column(db.String(15))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), unique=True, nullable=False)

    def __init__(self, fullname, bio, gender, phone, image):
        self.fullname = fullname
        self.bio = bio
        self.gender = gender
        self.phone = phone
        self.image = image

    def __repr__(self):
        return f'<Profile of User {self.user.username}>'