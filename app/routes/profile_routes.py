from datetime import datetime
from app import app, db
from flask import request, jsonify, send_file
from app.models import *
from app.static import *

# Create Profile
@app.route('/profile', methods=['POST'])
def create_profile():
    data = request.form
    if 'fullname' not in data or 'username' not in data:
        return jsonify({'error': 'Fullname, and username are required fields'}), 400
    try:
        fullname = data.get('fullname', '')
        bio = data.get('bio', '')
        gender = data.get('gender', '')
        phone = data.get('phone', '')
        location = data.get('location', '')
        username = data['username']

        user = get_user_by_username(username)
        
        if user is None:
            return jsonify({'error': 'User Not found'}), 404
        
        existed_profile = Profile.query.filter_by(user_id=user.id).first()
        if existed_profile:
            return jsonify({'error': 'Profile already exist'}), 400
    

        profile = Profile(
            fullname=fullname,
            bio=bio,
            gender=gender,
            phone=phone,
            location=location,
            user_id=user.id
        )
        db.session.add(profile)
        db.session.commit()

        if 'profile_picture' in request.files:
            image_file = request.files['profile_picture']
            image_data = image_file.read()
            image_name = image_file.filename
            image_extension = image_name.rsplit('.', 1)[1].lower() if '.' in image_name else ''

            image_entity_type = ImageEntityType.query.filter_by(entity_name=EntityTypes.Profile).first()  

            if not image_entity_type:
                return jsonify({'error': 'Image Entity Type ID not found for the given entity name'}), 404
            
            image = Image(
                data=image_data,
                image_name=image_name,
                image_extension=image_extension,
                entity_id=profile.id,
                entity_type_id=image_entity_type.id,
                created_date=datetime.utcnow()
            )
            db.session.add(image)
            db.session.commit()
        return jsonify({'error': 'Profile created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
    
#Get Profile
@app.route('/profile/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    profile = Profile.query.get(profile_id)
    
    if profile:
        image_entity_type = ImageEntityType.query.filter_by(entity_name=EntityTypes.Profile).first()
        image = Image.query.filter_by(entity_id=profile.id, entity_type_id=image_entity_type.id).first() 
        
        image_json = image.to_dict() if image else None
        
        return jsonify({
            'id': profile.id,
            'fullname': profile.fullname,
            'bio': profile.bio,
            'gender': profile.gender,
            'phone': profile.phone,
            'location': profile.location,
            'user_id': profile.user_id,
            'profile_picture': image_json
        })
    else:
        return jsonify({'error': 'Profile not found'}), 404

# Update Profile
@app.route('/profile/<int:profile_id>', methods=['PUT'])
def update_profile(profile_id):
    data = request.form
    profile = Profile.query.get(profile_id)
    if profile:
        try:
            profile.fullname = data.get('fullname', profile.fullname)
            profile.bio = data.get('bio', profile.bio)
            profile.gender = data.get('gender', profile.gender)
            profile.phone = data.get('phone', profile.phone)
            profile.location = data.get('location', profile.location)
            
            db.session.commit()
            if request.files['profile_picture']:
                new_image = request.files['profile_picture']
                image_entity_type = ImageEntityType.query.filter_by(entity_name=EntityTypes.Profile).first()
                image = Image.query.filter_by(entity_id=profile.id, entity_type_id=image_entity_type.id).first()  # Assuming entity_type_id for Profile is 1
                if image:
                    image.data = new_image.read()
                    image.image_name = new_image.filename
                    image.image_extention = new_image.filename.rsplit('.', 1)[1].lower() if '.' in image.image_name else ''
                    db.session.commit()
                else:
                    image_data = new_image.read()
                    image_name = new_image.filename
                    image_extension = image_name.rsplit('.', 1)[1].lower() if '.' in image_name else ''
                    image = Image(
                        data=image_data,
                        image_name=image_name,
                        image_extension=image_extension,
                        entity_id=profile.id,
                        entity_type_id=image_entity_type.id,
                        created_date=datetime.utcnow()
                    )
                    db.session.add(image)
                    db.session.commit()
            
            return jsonify({'message': 'Profile updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Profile not found'}), 404

# Delete Profile
@app.route('/profile/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    profile = Profile.query.get(profile_id)
    
    if profile:
        try:
            db.session.delete(profile)
            db.session.commit()
            
            image_entity_type = ImageEntityType.query.filter_by(entity_name=EntityTypes.Profile).first()
            image = Image.query.filter_by(entity_id=profile.id, entity_type_id=image_entity_type.id).first()
            if image:
                db.session.delete(image)
                db.session.commit()

            return jsonify({'message': 'Profile deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Profile not found'}), 404