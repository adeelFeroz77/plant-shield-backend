import requests
from app import db, app
from datetime import datetime, timedelta
from app.models.plant import Plant
from app.routes import auth_routes, user_plant_routes


firebase_url = "https://fcm.googleapis.com/fcm/send"
server_key = "AAAADLC-ndo:APA91bF213VrUn1-f_3Yl7mo149p5_RwsZ6wK7ZgJ3lmLsM3FInlx8gGJ5bNDt5PqdUyeYXmEZlSjtAoRSFC8GXo3LpfzWi1727Kjjs1j6_xl_4j0yRpYVwCzST14KehNP9whZ8PVb_S"
headers = {
    'Authorization' : f'key={server_key}',
    'Content-Type': 'application/json'
}

def schedule_notification():
    with app.app_context():
        try:
            users = auth_routes.get_all_users()
            # print(users)
            for user in users:
                device_token = user.device_token
                # print(device_token)

                if device_token is None or device_token.strip() == '':
                    continue

                username = user.username
                user_plants = user_plant_routes.get_user_plants_by_username(username=username)
                for user_plant in user_plants:
                    last_watered = user_plant.last_watered
                    plant = Plant.query.get(user_plant.plant_id)
                    unit = "hours"
                    watering_time = float(plant.watering_schedule)
                    time = last_watered + timedelta(hours=watering_time)
                    if watering_time < 1:
                        watering_time = round(watering_time * 60)
                        unit = "minutes"
                    if time <= datetime.utcnow():
                        body = {
                            'notification': {
                                'title': 'Your Plant is Thirsty!',
                                'body': f'Time to water {plant.plant_name}. It\'s been {watering_time} {unit}'
                            },
                            'data' : {
                                'plant_name': plant.plant_name,
                            },
                            'to': device_token
                        }

                        # print(body)

                        response = requests.post(firebase_url, headers= headers, json=body)
                        # print(response.json)
        except Exception as e:
            pass


                
            
                
