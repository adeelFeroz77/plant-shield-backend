from datetime import datetime
from app import app, db
from flask import request, jsonify, send_file
from app.models import *
from app.static import *
from app.routes import *
from app.exceptions import *
from sqlalchemy import func

# add new disease info
@app.route('/disease', methods=['POST'])
def add_disease():
    data = request.form
    try:
        disease_name = data.get('disease_name', '')
        description = data.get('description', '')
        possible_steps = data.get('possible_steps', '')

        if disease_name == '' or disease_name is None:
            return jsonify({'error': 'Disease name connot be emtpy or null'}) , 400
        
        existing_disease = DiseaseInfo.query.filter_by(name = disease_name).first()

        if existing_disease is not None:
            return jsonify({'error': 'Disease already exist.'}), 400

        new_disease = DiseaseInfo(
            name=disease_name,
            description=description,
            possible_steps=possible_steps
        )
        db.session.add(new_disease)
        db.session.commit()

        return jsonify({'success':'Disease added successfully'}),200

    except EntityTypeException as e:
        db.session.rollback()
        return jsonify({'Entity Error' : e.message}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Read all disease
@app.route('/disease', methods=['GET'])
def get_all_disease():
    try:
        diseases = DiseaseInfo.query.all()
        disease_list = [
                {
                    'id': disease.id,
                    'disease_name': disease.name,
                    'disease_description': disease.description,
                    'possible_steps': disease.possible_steps,
                }
                for disease in diseases
            ]
        return jsonify({'Diseases': disease_list}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500

# Read a specific disease
@app.route('/disease/<int:disease_id>', methods=['GET'])
def get_disease_by_id(disease_id):
    try:
        disease = DiseaseInfo.query.get(disease_id)

        disease_data = {
            'id': disease.id,
            'disease_name': disease.name,
            'description': disease.description,
            'possible_steps': disease.possible_steps
        }
        return jsonify({'Disease': disease_data}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500

def get_disease_by_name(disease_name):
    disease = DiseaseInfo.query.filter(func.lower(DiseaseInfo.name) == disease_name.lower()).first()
    return disease
