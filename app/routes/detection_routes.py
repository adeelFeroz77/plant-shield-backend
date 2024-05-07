from datetime import datetime, timedelta
from app import app, db
from flask import request, jsonify, send_file
from app.models import *
from app.static import *
from app.routes import image_routes, auth_routes
from app.exceptions import *


@app.route('/detections/<string:username>', methods=['GET'])
def get_last_detections(username):

    try:
        if not username:
            return jsonify({'error':'Username cannot be null'}), 400
        
        user_id = auth_routes.get_user_id_by_username(username)

        if not user_id:
            return jsonify({'error':'User not found'}), 404

        detections = DetectionHistory.query.\
            filter (DetectionHistory.user_id == user_id,
                    DetectionHistory.is_accurate_prediction == None,
                    DetectionHistory.timestamp < datetime.utcnow() - timedelta(days=7))
        image_entity_type = ImageEntityType.query.filter_by(entity_name=EntityTypes.UserPlant).first()

        detection_list = []

        for detection in detections:

            image = Image.query.filter_by(entity_id=detection.user_plant_id, entity_type_id=image_entity_type.id).first()
            image_json = image.to_dict() if image else None
            disease = DiseaseInfo.query.get(detection.detected_disease)
            plant = Plant.query.get(detection.plant_id)
            detection_data = {
                'id': detection.id,
                'plant_name': plant.plant_name,
                'disease': disease.name,
                'timestamp': detection.timestamp,
                'image': image_json
            }

            detection_list.append(detection_data)

        return jsonify({'Detections': detection_list}),200
    except Exception as e:
        return jsonify({'error': str(e)}),500
    
# Get feedback of last detection
@app.route('/detections/<int:detection_id>', methods=['PUT'])
def update_detection(detection_id):
    data = request.form
    detection = DetectionHistory.query.get(detection_id)
    if detection:
        try:
            res = data.get('is_accurate_prediction', detection.is_accurate_prediction)
            if res:
                res = bool(res)
            detection.is_accurate_prediction = res
            db.session.commit()
            return jsonify({'message': 'Detection\'s feedback updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500    
    else:
        return jsonify({'error': 'No Detection found'}), 404