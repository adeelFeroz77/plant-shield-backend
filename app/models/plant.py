from app import db
import datetime

class Plant(db.Model):
    __tablename__ = 'plant'
    id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    species = db.Column(db.String(100))
    watering_schedule = db.Column(db.String(50))
    sunlight_requirements = db.Column(db.String(50))
    temperature_requirements = db.Column(db.String(50))
    care_instructions = db.Column(db.Text)
    notes = db.Column(db.Text)
    is_favorite = db.Column(db.Boolean, default=False)
    is_blooming = db.Column(db.Boolean, default=False)
    tags = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, plant_name, description, species, watering_schedule,sunlight_requirements,temperature_requirements,care_instructions,notes,is_favorite,is_blooming,tags,created_date):
        self.plant_name = plant_name
        self.description = description
        self.species = species
        self.watering_schedule = watering_schedule
        self.sunlight_requirements=sunlight_requirements
        self.temperature_requirements=temperature_requirements
        self.care_instructions=care_instructions
        self.notes=notes
        self.is_favorite=is_favorite
        self.is_blooming=is_blooming
        self.tags=tags
        self.created_date=created_date

    def __repr__(self):
        return f'<Plant {self.plant_name}>'