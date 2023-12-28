from flask_login import login_user
from app import app, db, bcrypt
from flask import request, jsonify
from app.models import *
import re
from datetime import datetime

@app.route('/register',methods=['POST'])
def register_user():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

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
        created_date=datetime.utcnow()
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
            return jsonify({'message': "Choose new password, This is your previous password"}), 400
        
        hash_new_pass = bcrypt.generate_password_hash(new_password).decode('utf-8')

        user.password = hash_new_pass
        db.session.commit()

        save_password_history(user_id=user.id,password_hash=hash_new_pass)

        return jsonify({"message": "Your password has been changed"}), 200
    else:
        return jsonify({'message': "Invalid JSON data provided"}), 401

def save_password_history(user_id,password_hash):
    timestamp = datetime.utcnow()

    password_history = PasswordHistory(
        user_id=user_id,
        password_hash=password_hash,
        timestamp=timestamp
    )
    db.session.add(password_history)
    db.session.commit()

@app.route('/signin', methods=['POST'])
def signin_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401
    # login_user(user=user, remember=True)
    return jsonify({'message': 'SignIn successful'}), 200