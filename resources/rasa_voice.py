from flask_restful import Resource
from flask import request, jsonify, send_file
import requests, datetime
from gtts import gTTS
from models.chat import ChatModel

class RasaVoice(Resource):
    def get(self):
        return jsonify({"message": "make a post request for VOICE mp3 result"})
    
    def post(self):
        username = request.get_json()['username']
        text = request.get_json()['text']
        
        url = 'http://0.0.0.0:5005/webhooks/rest/webhook'
        
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
            return {"error messages": "Not Any including response for this conversation query"}
        tts = gTTS(result.json()[0]['text'], lang='en', tld="com")
        file_name = f'audios/rasa-{hash(tts)}.mp3'
        tts.save(file_name)
        
        print("*"*40)
        print(result.json())
        print("*"*40)
        
        return send_file(file_name, mimetype="audio/mp3")