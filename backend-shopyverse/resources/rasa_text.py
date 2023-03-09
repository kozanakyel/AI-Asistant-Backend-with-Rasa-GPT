from flask_restful import Resource
from flask import request, jsonify
import requests, datetime, json
from models.chat import ChatModel
import config


class RasaText(Resource):
    def get(self):
        return jsonify({"message": "make a post request for result"})
    
    def post(self):
        username = request.get_json()['username']
        text = request.get_json()['text']
        
        url = config.RASA_SERVER
        
        data = {
            "sender": username,
            "message": text
        }
        data_chat = {
            "text": request.get_json()['text'],
            "username": request.get_json()['username'],
            "publish_date": datetime.datetime.now()
        }
        
        chat = ChatModel(**data_chat)  # since parser only takes in username and password, only those two will be added.
        chat.save_to_database()
        
        result = requests.post(url=url, json=data)
        
        if result.json() == []:
            return {"error": "Yet I'm not trained for this!"}, 402
        
        print("*"*40)
        print(result.json())
        print("*"*40)
        
        return result.json(), 201