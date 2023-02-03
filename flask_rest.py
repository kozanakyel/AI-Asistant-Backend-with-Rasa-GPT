import requests
from dotenv import load_dotenv
import os
import openai

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

load_dotenv()

CHATGPT_ENV=os.getenv('CHATGPT')
openai.api_key = CHATGPT_ENV

app = Flask(__name__)
CORS(app)

#Creating  api instance
api = Api(app)

class Rasa(Resource):
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
        print("*"*40)
        print(result.json())
        print("*"*40)
        
        return result.json()
    
class GptText(Resource):
    def get(self):
        return jsonify({"message": "Response CHATGPT post a text"})
    
    def post(self):
        question = request.get_json()['question']
        
        print(f'Question : {question}')
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=256,
            n=1
        )
        
        
        response_text = response['choices'][0]['text']
        print("*"*40)
        print(f'GPT TEXT response: {response_text.json()}')
        print("*"*40)
        
        return jsonify(response_text)
    
api.add_resource(Rasa, '/rasachat')
api.add_resource(GptText, '/gpttext')
    
if __name__ == '__main__':
    app.run(debug=True)
        