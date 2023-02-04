from flask_restful import Resource
from flask import request, jsonify
import requests

class RasaText(Resource):
    def get(self):
        return jsonify({"message": "make a post request for result"})
    
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
        
        print("*"*40)
        print(result.json())
        print("*"*40)
        
        return result.json()