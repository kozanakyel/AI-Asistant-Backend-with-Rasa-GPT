from flask_restful import Resource
from flask import request, jsonify
import requests

class RasaText(Resource):
    def get(self):
        return jsonify({"message": "make a post request for result"})
    
    def post(self):
        username = request.get_json()['username']
        text = request.get_json()['text']
        
        url = 'http://0.0.0.0:5005/webhooks/rest/webhook'
        
        data = {
            "sender": username,
            "message": text
        }
        
        result = requests.post(url=url, json=data)
        
        if result.json() == []:
            return {"error messages": "Not Any including response for this conversation query"}
        
        print("*"*40)
        print(result.json())
        print("*"*40)
        
        return result.json()