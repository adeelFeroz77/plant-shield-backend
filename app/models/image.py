from app import db

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)
    entity_id = db.Column(db.Integer, nullable=False)
    entity_type_id = db.Column(db.Integer, db.ForeignKey('image_entity_type.id'), nullable=False)
    
    def __init__(self, data, entity_id, entity_type_id):
        self.data = data
        self.entity_id = entity_id
        self.entity_type_id = entity_type_id

    def __repr__(self):
        return f'<image {self}>'