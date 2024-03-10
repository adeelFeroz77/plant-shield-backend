from datetime import datetime
from app import app, db
from flask import request, jsonify, send_file
from app.models import *
from app.static import *
from app.routes import image_routes, plant_routes, auth_routes
from app.exceptions import *

@app.route('/user-plant/<int:user_id>/<int:plant_id>', methods=['POST'])
def add_user_plant(plant_id, user_id):
    plant = Plant.query.get(plant_id)
    user = User.query.get(user_id)

    if not plant:
        return jsonify({'error' , "Plant not found"}), 404
    if not user:
        return jsonify({'error' , "User not found"}), 404
    