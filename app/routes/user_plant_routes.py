import base64
from datetime import datetime
import os
from app import app, db
from flask import request, jsonify, send_file
from app.models import *
from app.static import *
from app.routes import image_routes, plant_routes, auth_routes, disease_routes
from app.exceptions import *
from app.detection_model import image_detection

@app.route('/user-plant', methods=['POST'])
def add_user_plant():
    data = request.form

    try:
        plant_id = data.get('plant_id',-1)
        username = data.get('username',-1)
        last_watered = data.get('last_watered', datetime.utcnow())
        notes = data.get('notes', '')
        current_disease = data.get('current_disease', 'Healthy')

        plant = Plant.query.get(plant_id)
        user = User.query.filter_by(username = username).first()  
        disease = disease_routes.get_disease_by_name(current_disease)

        if not plant:
            return jsonify({'error' , "Plant not found"}), 404
        if not user:
            return jsonify({'error' , "User not found"}), 404
        if not disease:
            return jsonify({'error': 'Disease not found'}), 404
        
        user_plant = UserPlant(
            user_id= user.id,
            plant_id = plant.id,
            last_watered = last_watered,
            notes = notes,
            current_disease = disease.id
        )
        db.session.add(user_plant)
        db.session.commit()

        if 'user_plant_image' in request.files:
            image_file = request.files['user_plant_image']
            image_routes.save_image_by_entity_and_entity_type(image_file,user_plant.id, EntityTypes.UserPlant)

            # print(user_plant.id)
            detection_history = DetectionHistory(
                user_id= user.id,
                plant_id= plant.id,
                user_plant_id = user_plant.id,
                detected_disease= disease.id,
                is_accurate_prediction= None,
                timestamp= None
            )

            db.session.add(detection_history)
            db.session.commit()

        return jsonify({'message': 'Plant added in User\'s list'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}),500


@app.route('/detect-plant', methods = ['GET'])    
def detect_plant():
    data = request.form
    try:
        if 'plant_image' in request.files:
            image_file = request.files['plant_image']
            pred = image_detection.predict_image(image_file)
            pred_info = image_detection.getDiseaseInfo(pred)
            # print(pred_info)
            if not ":" in pred_info:
                return jsonify({'message': 'No Plant detected in provided image'}), 400

            plant_name = pred_info.split(':')[0].strip()
            disease_name = pred_info.split(':')[1].strip()
            plant = plant_routes.get_plant_by_name(plant_name)
            disease = disease_routes.get_disease_by_name(disease_name)

            if not plant:
                return jsonify({'message': 'Plant not found in Database'}), 404
            
            if not disease:
                return jsonify({'message': 'Disease not found in Database'}), 404

            obj = {
                'plant_id': plant.id,
                'plant_name': plant.plant_name,
                'description': plant.description,
                'species': plant.species,
                'species_detail': plant.species_detail,
                'max_life': plant.max_life,
                'watering_schedule': plant.watering_schedule,
                'watering_schedule_detail': plant.watering_schedule_detail,
                'sunlight_requirements': plant.sunlight_requirements,
                'sunlight_requirements_detail': plant.sunlight_requirements_detail,
                'temperature_requirements': plant.temperature_requirements,
                'temperature_requirements_detail': plant.temperature_requirements_detail,
                'humidity': plant.humidity,
                'humidity_detail': plant.humidity_detail,
                'notes': plant.notes,
                'disease_name': disease.name,
                'disease_description': disease.description,
                'disease_possible_steps': disease.possible_steps
            }

            return jsonify(obj), 200
        else:
            return jsonify({'message': 'Image not attached'}), 400
    except Exception as e:
        return jsonify({'exception': str(e)}), 500
    
# Get all added plants of a user
@app.route('/user-plants/<string:username>', methods=['GET'])
def get_all_added_plants_of_user(username):
    try:
        if not username:
            return jsonify({'error':'Username cannot be null'}), 400
        
        user_id = auth_routes.get_user_id_by_username(username)

        if not user_id:
            return jsonify({'error':'User not found'}), 404

        user_plants = UserPlant.query.filter_by(user_id = user_id)
        image_entity_type = ImageEntityType.query.filter_by(entity_name=EntityTypes.UserPlant).first()

        if user_plants is None:
            return jsonify({'error': 'No plants added'}), 404
        
        user_plant_list = []

        for user_plant in user_plants:
            image = Image.query.filter_by(entity_id=user_plant.id, entity_type_id=image_entity_type.id).first()
            image_json = base64.b64encode(image.get_data()).decode('utf-8') if image else None
            plant = Plant.query.get(user_plant.plant_id)
            disease = DiseaseInfo.query.get(user_plant.current_disease)
            plant_data = {
                'id': user_plant.id,
                'plant_name': plant.plant_name,
                'species': plant.species,
                'watering_schedule': plant.watering_schedule,
                'user_plant_image': image_json,
                'current_disease': disease.name,
                'last_watered': user_plant.last_watered
            }
            user_plant_list.append(plant_data)

        return jsonify({'User Plants': user_plant_list}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Get user plany by username and id
@app.route('/user-plants/<string:username>/<int:userplant_id>', methods=['GET'])
def get_user_plant_by_username_and_id(username,userplant_id):
    try:
        if not username:
            return jsonify({'error':'Username cannot be null'}), 400
        
        if not userplant_id:
            return jsonify({'error':'UserPlant id cannot be null'}), 400
        
        user_id = auth_routes.get_user_id_by_username(username)

        if not user_id:
            return jsonify({'error':'User not found'}), 404

        user_plant = UserPlant.query.filter_by(user_id = user_id, id=userplant_id).first()
        image_entity_type = ImageEntityType.query.filter_by(entity_name=EntityTypes.UserPlant).first()

        if user_plant is None:
            return jsonify({'error': 'User Plant not found'}), 404

        image = Image.query.filter_by(entity_id=user_plant.id, entity_type_id=image_entity_type.id).first()
        image_json = base64.b64encode(image.get_data()).decode('utf-8') if image else None
        plant = Plant.query.get(user_plant.plant_id)
        disease = DiseaseInfo.query.get(user_plant.current_disease)
        plant_data = {
            'id': user_plant.id,
            'plant_name': plant.plant_name,
            'description': plant.description,
            'species': plant.species,
            'species_detail': plant.species_detail,
            'max_life': plant.max_life,
            'watering_schedule': plant.watering_schedule,
            'watering_schedule_detail': plant.watering_schedule_detail,
            'sunlight_requirements': plant.sunlight_requirements,
            'sunlight_requirements_detail': plant.sunlight_requirements_detail,
            'temperature_requirements': plant.temperature_requirements,
            'temperature_requirements_detail': plant.temperature_requirements_detail,
            'humidity': plant.humidity,
            'humidity_detail': plant.humidity_detail,
            'notes': plant.notes,
            'user_plant_image': image_json,
            'current_disease': disease.name,
            'disease_description': disease.description,
            'disease_possible_steps': disease.possible_steps,
            'last_watered': user_plant.last_watered,
            'date_added': user_plant.date_added
        }

        return jsonify({'User Plant': plant_data}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/user-plants/<string:username>/<int:userplant_id>', methods=['PUT'])
def update_user_plant(username, userplant_id):
    data = request.form
    try:
        if not username:
            return jsonify({'error':'Username cannot be null'}), 400
        
        if not userplant_id:
            return jsonify({'error':'UserPlant id cannot be null'}), 400
        
        user_id = auth_routes.get_user_id_by_username(username)

        if not user_id:
            return jsonify({'error':'User not found'}), 404
        
        user_plant = UserPlant.query.filter_by(user_id = user_id, id=userplant_id).first()

        if not user_plant:
            return jsonify({'error': 'User plant not found'}), 404
        
        last_watered = data.get('last_watered')
        if not last_watered is None and last_watered.lower() == "now":
            user_plant.last_watered = datetime.utcnow()
        user_plant.notes = data.get('notes', user_plant.notes)
        updated_disease = disease_routes.get_disease_by_name(data.get('current_disease',''))
        if updated_disease:
            user_plant.current_disease = updated_disease.id
        db.session.commit()

        if 'user_plant_image' in request.files:
            new_image = request.files['user_plant_image']
            old_image = image_routes.get_image_by_entity_id_and_entity_type(entity_id=user_plant.id, entity_name=EntityTypes.UserPlant)
            if old_image:
                image_routes.update_image(old_image= old_image, new_image= new_image)
            else:
                image_routes.save_image_by_entity_and_entity_type(image_file=new_image, entity_id=user_plant.id, entity_name=EntityTypes.UserPlant)
        
        return jsonify({'success': 'User plant updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Failed to updated user plant': str(e)}), 500
    

# Delete specific user-plant
@app.route('/user-plants/<string:username>/<int:userplant_id>', methods=['DELETE'])
def delete_user_plant(username, userplant_id):
    data = request.form
    try:
        if not username:
            return jsonify({'error':'Username cannot be null'}), 400
        
        if not userplant_id:
            return jsonify({'error':'UserPlant id cannot be null'}), 400
        
        user_id = auth_routes.get_user_id_by_username(username)

        if not user_id:
            return jsonify({'error':'User not found'}), 404
        
        user_plant = UserPlant.query.filter_by(user_id = user_id, id=userplant_id).first()

        if not user_plant:
            return jsonify({'error': 'User plant not found'}), 404
        
        db.session.delete(user_plant)
        db.session.commit()

        image = image_routes.get_image_by_entity_id_and_entity_type(entity_id=userplant_id, entity_name=EntityTypes.UserPlant)
        if image:
            db.session.delete(image)
            db.session.commit()
        
        return jsonify({'success': 'User plant deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Failed to delete user plant': str(e)}), 500
    
def get_user_plants_by_username(username):
    try:
        user_id = auth_routes.get_user_id_by_username(username)
        user_plants = UserPlant.query.filter_by(user_id = user_id)
        return user_plants
    except Exception as e:
        return []