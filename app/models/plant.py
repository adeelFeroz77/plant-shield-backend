from app import db
from datetime import datetime
from sqlalchemy.sql import func

class Plant(db.Model):
    __tablename__ = 'plant'
    id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    species = db.Column(db.String(100))
    species_detail = db.Column(db.Text)
    max_life = db.Column(db.Text)
    watering_schedule = db.Column(db.String(100))
    watering_schedule_detail = db.Column(db.Text)
    sunlight_requirements = db.Column(db.String(100))
    sunlight_requirements_detail = db.Column(db.Text)
    temperature_requirements = db.Column(db.String(100))
    temperature_requirements_detail = db.Column(db.Text)
    humidity = db.Column(db.String(100))
    humidity_detail = db.Column(db.Text)
    notes = db.Column(db.Text)
    is_favorite = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, server_default=func.now())

    def __init__(self, plant_name, description, species,species_detail, max_life, watering_schedule, watering_schedule_detail, sunlight_requirements,sunlight_requirements_detail,temperature_requirements,temperature_requirements_detail,humidity,humidity_detail,notes,is_favorite,created_date):
        self.plant_name = plant_name
        self.description = description
        self.species = species
        self.species_detail = species_detail
        self.max_life = max_life
        self.watering_schedule = watering_schedule
        self.watering_schedule_detail = watering_schedule_detail
        self.sunlight_requirements=sunlight_requirements
        self.sunlight_requirements_detail = sunlight_requirements_detail
        self.temperature_requirements=temperature_requirements
        self.temperature_requirements_detail = temperature_requirements_detail
        self.humidity = humidity
        self.humidity_detail = humidity_detail
        self.notes=notes
        self.is_favorite=is_favorite
        self.created_date=created_date

    def __repr__(self):
        return f'<Plant {self.plant_name}>'