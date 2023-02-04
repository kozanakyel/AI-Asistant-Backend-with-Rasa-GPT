from flask_restful import Resource
from flask import request, jsonify, send_file
import requests
from gtts import gTTS

class RasaVoice(Resource):
    def get(self):
        return jsonify({"message": "make a post request for VOICE mp3 result"})
   
    def post(self):
        id = request.get_json()['id']
        msg = request.get_json()['msg']
        
        url = 'http://0.0.0.0:5005/webhooks/rest/webhook'
        
        data = {
            "sender": id,
            "message": msg
        }
        
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