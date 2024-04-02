from app import mail
from flask_mail import Message

def send_otp_over_mail(recepient_mail, otp_code):
    message =\
    """
    Greetings!

    To continue with your registration, here's your OTP to be entered: %d

    Do not share this OTP with anyone else.

    Regards,
    Team PlantShield
    """ % (otp_code)

    mail_message = Message(
        subject= "Plant Shield OTP Verification",
        recipients = [recepient_mail],
        body=message
    )
    
    mail.send(mail_message)
