from app import app, db, bcrypt
from flask import request, jsonify
from app.models.user import *

@app.route('/signup',methods=['POST'])
def signup_user():
    data = request.get_json()
    if data:
        print(data)
        user = User(
            email=data.get('email'),
            username=data.get('username'),
            password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
        )
        print(user)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User added successfully"}), 200
    else:
        return jsonify({'message': "Invalid JSON data provided"}), 401
    

@app.route('/signin', methods=['POST'])
def signin_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'SignIn successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401