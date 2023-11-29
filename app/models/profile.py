from app import db

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.String(500))
    gender = db.Column(db.String(6))
    phone = db.Column(db.String(15))
    image = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), unique=True, nullable=False)
    # user = db.relationship('User', backref=db.backref('profile', uselist=False), lazy=True)

    def __init__(self, fname, lname, bio, gender, phone, image):
        self.fname = fname
        self.lname = lname
        self.bio = bio
        self.gender = gender
        self.phone = phone
        self.image = image

    def __repr__(self):
        return f'<Profile of User {self.user.username}>'