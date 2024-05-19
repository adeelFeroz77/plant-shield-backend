import base64
from flask_login import login_user
from app import app, db, bcrypt
from flask import request, jsonify
from app.models import *
import re
from datetime import datetime
from app.static.enums import EntityTypes

@app.route('/validate-new-user',methods=['GET'])
def validate_user():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password or not email:
        return jsonify({"error": "Email,Username and password are required"}), 400
    
    validation_result = validate_new_user(email=email, username=username, password=password)

    if validation_result is not None:
        return validation_result
    
    return jsonify({"message": "User Validate Successfully"}), 200
    
@app.route('/register',methods=['POST'])
def register_user():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    device_token = request.form.get('device_token','')

    if not username or not password or not email:
        return jsonify({"error": "Email,Username and password are required"}), 400
    
    validation_result = validate_new_user(email=email, username=username, password=password)

    if validation_result is not None:
        return validation_result
    
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User(
        email=email,
        username=username,
        password=hash_password,
        created_date=datetime.utcnow(),
        device_token= device_token
    )
    db.session.add(user)
    db.session.commit()
    
    save_password_history(user_id=user.id,password_hash=hash_password)

    return jsonify({"message": "User added successfully"}), 200


def validate_new_user(email,username,password):
    if not is_valid_email(email):
        return jsonify({"error": "Email is not valid"}), 400
    
    if not is_valid_password(password):
        return jsonify({"error": "Password is not valid"}), 400

    existing_user_by_email = User.query.filter_by(email=email).first()
    if existing_user_by_email:
        return jsonify({"error": "An account is already exist with this Email, please try with another one."}), 400

    existing_user_by_username = User.query.filter_by(username=username).first()
    if existing_user_by_username:
        return jsonify({"error": "That username already exists. Please choose a different one."}), 400


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    match = re.match(pattern, email)
    return bool(match)

def is_valid_password(password):
    if len(password) < 8:
        return False
    
    if not any(char.isupper() for char in password):
        return False
    
    if not any(char.islower() for char in password):
        return False
    
    if not any(char.isdigit() for char in password):
        return False
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True

@app.route('/update/password',methods=['PUT'])
def update_password():
    new_password = request.form.get('new_password')
    username = request.form.get('username')
    if new_password and username:

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User does not exist."}), 400

        if not is_valid_password(new_password):
            return jsonify({"error": "Password is not valid"}), 400


        if any(bcrypt.check_password_hash(password_history.password_hash, new_password) for password_history  in PasswordHistory.query.filter_by(user_id=user.id)):
            return jsonify({'error': "Choose new password, This is your previous password"}), 400
        
        hash_new_pass = bcrypt.generate_password_hash(new_password).decode('utf-8')

        user.password = hash_new_pass
        db.session.commit()

        save_password_history(user_id=user.id,password_hash=hash_new_pass)

        return jsonify({"message": "Your password has been changed"}), 200
    else:
        return jsonify({'error': "Invalid JSON data provided"}), 401

def save_password_history(user_id,password_hash):
    timestamp = datetime.utcnow()

    password_history = PasswordHistory(
        user_id=user_id,
        password_hash=password_hash,
        timestamp=timestamp
    )
    db.session.add(password_history)
    db.session.commit()

@app.route('/login', methods=['POST'])
def signin_user():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        device_token = request.form.get('device_token')
        
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        if not device_token:
            return jsonify({'error': 'Device token is required'}), 400

        user = User.query.filter_by(username=username).first()
        
        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        existing_device_token = user.device_token

        if not existing_device_token is None and not existing_device_token.strip() == '':
            return jsonify({'error': 'User already logged in from another device'}), 400
        
        user.device_token = device_token
        db.session.commit()
        # login_user(user=user, remember=True)
        return jsonify({'message': 'SignIn successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/get-loggedin-user/<string:username>', methods=['GET'])
def get_loggedIn_user(username):
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user,profile = db.session.query(User, Profile).outerjoin(Profile).filter(User.username == username).first()
    if not user:
        return jsonify({'error': 'Invalid username'}), 401
    if profile:
        image_entity_type = ImageEntityType.query.filter_by(entity_name=EntityTypes.Profile).first()
        image = Image.query.filter_by(entity_id=profile.id, entity_type_id=image_entity_type.id).first()
    user_details = {
        'first_name': profile.first_name if profile else None,
        'last_name': profile.last_name if profile else None,
        'email': user.email,
        'username': user.username,
        'profile_picture': base64.b64encode(image.get_data()).decode('utf-8') if image else None,
        'device_token': user.device_token
    }
    return jsonify(user_details), 200

@app.route('/user/check-existence/<string:username>', methods=['GET'])
def check_user_existence(username):
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({"exists": True, "email": user.email}), 200
    else:
        return jsonify({"exists": False}), 200
    
@app.route('/user/validate-current-password', methods=['GET'])
def validate_current_password():
    username = request.form.get('username')
    curr_password = request.form.get('curr_password')
    
    if not curr_password:
        return jsonify({"error": "Current password is required"}), 400

    user = User.query.filter_by(username=username).first()
    
    if not user or not bcrypt.check_password_hash(user.password, curr_password):
        return jsonify({'error': 'Invalid current password'}), 401
    return jsonify({'message': 'Current password matched successfully'}), 200

@app.route('/logout/<string:username>', methods=['PUT'])
def logout_user(username):
    try:
        user = User.query.filter_by(username=username).first()
        
        if not user :
            return jsonify({'error': 'User not found'}), 404
        
        if user.device_token is None or user.device_token.strip() == '':
            return jsonify({'error': 'User already logged out'}), 400
        
        user.device_token = None
        db.session.commit()
        
        return jsonify({'message':'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_user_id_by_username(username):
    if not username:
        return None
    user = User.query.filter_by(username = username).first()
    if not user:
        return None
    return user.id

def get_all_users():
    try:
        users = User.query.all()
        return users
    except Exception as e:
        return []