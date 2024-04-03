from datetime import datetime, timedelta
from app import app, db
from flask import request, jsonify
from app.models import *
from app.routes import auth_routes
from app.service import mail_service


@app.route('/generate-otp', methods=['POST'])
def generate_otp():
    data = request.form
    try:
        email = data.get('user_email',None)

        if not email:
            return jsonify({'error': "Email is required!"}), 400
        
        if not auth_routes.is_valid_email(email):
            return jsonify({'error': "Enter a valid email"}), 400
        
        one_time_password = OneTimePassword(user_email= email)

        mail_service.send_otp_over_mail(recepient_mail= email, otp_code= one_time_password.otp_code)

        db.session.add(one_time_password)
        db.session.commit()

        return jsonify({
            'user_email': one_time_password.user_email,
            'otp': one_time_password.otp_code,
            'timestamp': one_time_password.timestamp
        }), 200
    
    except Exception as e:
        return jsonify({'exception': str(e)}), 500
    
@app.route('/verify-otp', methods=['GET'])
def verify_otp():
    data = request.form
    try:
        email = data.get('user_email',None)
        otp = int(data.get('otp', None))
        
        if not email:
            return jsonify({'error': "Email is required!"}), 400
        
        if not otp:
            return jsonify({'error': "OTP is required to validate"}), 400
        
        last_otp = OneTimePassword.query.\
            filter (OneTimePassword.user_email == email,
                    OneTimePassword.timestamp >= datetime.utcnow() - timedelta(minutes=5)).\
            order_by(OneTimePassword.timestamp.desc()).first()
        
        if not last_otp:
            return jsonify({'error': "Please generate OTP first"}), 404
        
        if int(last_otp.otp_code) != otp:
            return jsonify({'error': "OTP not verfied"}), 400
        
        return jsonify({'success': "User Verified!"}), 200
    
    except Exception as e:
        return jsonify({'exception': str(e)}), 500