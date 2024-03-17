from datetime import datetime
import os
from app import app, db
from flask import request, jsonify, send_file
from app.models import *
from app.static import *
from app.routes import image_routes, plant_routes, auth_routes
from app.exceptions import *
from app.detection_model import image_detection

@app.route('/user-plant', methods=['POST'])
def add_user_plant():
    data = request.form

    try:
        plant_id = data.get('plant_id',-1)
        user_id = data.get('user_id',-1)
        last_watered = data.get('last_watered', datetime.utcnow())
        notes = data.get('notes', '')
        current_disease = data.get('current_disease', 'Healthy')

        plant = Plant.query.get(plant_id)
        user = User.query.get(user_id)  

        if not plant:
            return jsonify({'error' , "Plant not found"}), 404
        if not user:
            return jsonify({'error' , "User not found"}), 404
        
        user_plant = UserPlant(
            user_id= user.id,
            plant_id = plant.id,
            last_watered = last_watered,
            notes = notes,
            current_disease = current_disease
        )
        db.session.add(user_plant)
        db.session.commit()

        disease = None

        if 'user_plant_image' in request.files:
            image_file = request.files['user_plant_image']
            image_routes.save_image_by_entity_and_entity_type(image_file,user_plant.id, EntityTypes.UserPlant)
            pred = image_detection.predict_image(image_file)
            disease = image_detection.getDiseaseInfo(pred)
            print(disease)
        
        if disease:
            UserPlant.current_disease = disease.split(':')[1].strip()
            db.session.commit()

        return jsonify({'message': 'Plant added in User\'s list'})
    except Exception as e:
        return jsonify({'error': str(e)}),500
    