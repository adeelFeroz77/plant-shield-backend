from app import app, db, bcrypt
from flask import request, jsonify
from app.models import *

@app.route('/image-entity-type',methods = ["Post"])
def add_image_entity_type():
    data = request.get_json()
    if data:
        entity_name = data.get('entity_name')
        if not entity_name:
            return jsonify({"error": "Entity Name Required"}), 400
        
        image_entity_type = ImageEntityType(
            entity_name=entity_name
        )
        db.session.add(image_entity_type)
        db.session.commit()
        return jsonify({"message": "Entity Type Added successfully"}), 200
    else:
        return jsonify({'message': "Invalid JSON data provided"}), 401