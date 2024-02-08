import base64
import datetime
from app import db

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary)
    image_name = db.Column(db.String(120))
    image_extension = db.Column(db.String(120))
    entity_id = db.Column(db.Integer, nullable=False)
    entity_type_id = db.Column(db.Integer, db.ForeignKey('image_entity_type.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __init__(self, data,image_name,image_extension, entity_id, entity_type_id,created_date):
        self.data = data
        self.image_name = image_name
        self.image_extension = image_extension
        self.entity_id = entity_id
        self.entity_type_id = entity_type_id
        self.created_date = created_date

    def __repr__(self):
        return f'<image {self}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'image_name':self.image_name,
            'image_extension':self.image_extension,
            'entity_id':self.entity_id,
            'entity_type_id':self.entity_type_id,
            'created_date':self.created_date.isoformat()
        }
    def get_data(self):
        return self.data