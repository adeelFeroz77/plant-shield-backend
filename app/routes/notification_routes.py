import requests
from app import db, app
from datetime import datetime, timedelta
from app.models.plant import Plant
from app.routes import auth_routes, user_plant_routes


firebase_url = "https://fcm.googleapis.com/fcm/send"
server_key = "" #Available after setup in firebase
headers = {
    'Authorization' : f'key={server_key}',
    'Content-Type': 'application/json'
}

def schedule_notification():
    body = {
            'notification': {
                'title': 'Your Plant is Thirsty!',
                'body': f'Time to water PlantNAme. It\'s been 2 hours'
            },
            'data' : {
                'plant_name': 'Test'
            },
            'token': "sdhasilfla"
        }

    print(body, headers)
    # users = auth_routes.get_all_users()
    # for user in users:
    #     device_token = user.device_token

    #     if device_token is None or device_token.str.trim().strip() == '':
    #         continue

    #     username = user.username
    #     user_plants = user_plant_routes.get_user_plant_by_username(username=username)
    #     for user_plant in user_plants:
    #         last_watered = user_plant.last_watered
    #         plant = Plant.query.get(id= user_plant.plant_id)
    #         watering_time = plant.watering_schedule
    #         time = last_watered + timedelta(hours=int(watering_time))
    #         if time <= datetime.utcnow():
    #             body = {
    #                 'notification': {
    #                     'title': 'Your Plant is Thirsty!',
    #                     'body': f'Time to water {plant.plant_name}. It\'s been {watering_time} hours'
    #                 },
    #                 'data' : {
    #                     'plant_name': plant.plant_name,
    #                 },
    #                 'token': device_token
    #             }

    #             print(body)

    #             response = requests.post(firebase_url, headers= headers, json=body)
    #             print(response.json)


                
            
                
