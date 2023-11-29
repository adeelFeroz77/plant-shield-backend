from app import app, db, bcrypt
from flask import request, jsonify
from app.models.user import *

@app.route('/register',methods=['POST'])
def register_user():
    data = request.get_json()

    if data:
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not username or not password or not email:
            return jsonify({"error": "Email,Username and password are required"}), 400
        
        existing_user_by_email = User.query.filter_by(email=email).first()
        if existing_user_by_email:
            return jsonify({"error": "An account is already exist with this Email, please try with another one."}), 400

        existing_user_by_username = User.query.filter_by(username=username).first()
        if existing_user_by_username:
            return jsonify({"error": "That username already exists. Please choose a different one."}), 400

        hash_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        user = User(
            email=email,
            username=username,
            password=hash_password,
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User added successfully"}), 200
    else:
        return jsonify({'message': "Invalid JSON data provided"}), 401
    

@app.route('/signin', methods=['POST'])
def signin_user():
    data = request.get_json()
    if data:
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        user = User.query.filter_by(username=username).first()
        
        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid username or password'}), 401
        
        return jsonify({'message': 'SignIn successful'}), 200
    else:
        return jsonify({'message':'Invalid JSON data provided'}), 401