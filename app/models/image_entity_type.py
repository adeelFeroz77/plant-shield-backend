from app import db

class ImageEntityType(db.Model):
    __tablename__ = 'image_entity_type'
    id = db.Column(db.Integer, primary_key=True)
    entity_name = db.Column(db.String(120), unique=True, nullable=False)
    image = db.relationship('Image', backref='image_entity_type', lazy=True)

    def __init__(self, entity_name):
        self.entity_name = entity_name

    def __repr__(self):
        return f'<image_entity_type {self}>'