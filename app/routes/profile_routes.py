import io
from app import app, db
from flask import request, jsonify, send_file
from app.models import *
from app.static import *

# Create Profile
@app.route('/profile', methods=['POST'])
def create_profile():
    data = request.form
    if 'image' not in request.files or 'fullname' not in data or 'user_id' not in data:
        return jsonify({'error': 'Image, fullname, and user_id are required fields'}), 400
    try:
        fullname = data.get('fullname', '')
        bio = data.get('bio', '')
        gender = data.get('gender', '')
        phone = data.get('phone', '')
        user_id = int(data['user_id'])
        profile = Profile(
            fullname=fullname,
            bio=bio,
            gender=gender,
            phone=phone,
            user_id=user_id
        )
        db.session.add(profile)
        db.session.commit()

        image_file = request.files['image']
        image_data = image_file.read()
        image_name = image_file.filename
        image_extension = image_name.rsplit('.', 1)[1].lower() if '.' in image_name else ''

        # Create and add image
        image_entity_type = ImageEntityType.query.filter_by(entity_name=EntityTypes.Profile).first()  # Change this to the appropriate image_entity_type_id for Profile
        
        if not image_entity_type:
            raise ValueError("Image Entity Type ID not found for the given entity name")
        
        image = Image(
            data=image_data,
            image_name=image_name,
            image_extension=image_extension,
            entity_id=profile.id,
            entity_type_id=image_entity_type.id
        )
        db.session.add(image)
        db.session.commit()
        return jsonify({'message': 'Profile created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/profile/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    profile = Profile.query.get(profile_id)
    
    if profile:
        image_entity_type = ImageEntityType.query.filter_by(entity_name=EntityTypes.Profile).first()
        image = Image.query.filter_by(entity_id=profile.id, entity_type_id=image_entity_type.id).first()  # Assuming entity_type_id for Profile is 1
        image_data = image.data if image else None
        
        return jsonify({
            'id': profile.id,
            'fullname': profile.fullname,
            'bio': profile.bio,
            'gender': profile.gender,
            'phone': profile.phone,
            'user_id': profile.user_id,
            'image_data': image_data
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
            
            db.session.commit()
            new_image = request.files['image']
            if new_image:
                image_entity_type = ImageEntityType.query.filter_by(entity_name=EntityTypes.Profile).first()
                image = Image.query.filter_by(entity_id=profile.id, entity_type_id=image_entity_type.id).first()  # Assuming entity_type_id for Profile is 1
                if image:
                    image.data = new_image.read()
                    image.image_name = new_image.filename
                    image.image_extention = new_image.filename.rsplit('.', 1)[1].lower() if '.' in image_name else ''
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
                        entity_type_id=image_entity_type.id
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
            image = Image.query.filter_by(entity_id=profile.id, entity_type_id=image_entity_type.id).first()  # Assuming entity_type_id for Profile is 1
            if image:
                db.session.delete(image)
                db.session.commit()

            return jsonify({'message': 'Profile deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Profile not found'}), 404
    
@app.route('/get-image')
def get_image():
    image = Image.query.filter_by(entity_id=1, entity_type_id=1).first()
    return send_file(io.BytesIO(image.data),
                             mimetype=f'image/{image.image_extension}',
                             as_attachment=True,
                             download_name=image.image_name)