import requests
from dotenv import load_dotenv
import os, shutil
import openai

from flask import Flask, request, jsonify, send_file
from flask_restful import Resource, Api
from flask_cors import CORS

from gtts import gTTS

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
        tts = gTTS(result.json()[0]['text'], lang='en', tld="com")
        file_name = f'audios/rasa-{hash(tts)}.mp3'
        tts.save(file_name)
        
        print("*"*40)
        print(result.json())
        print("*"*40)
        
        return send_file(file_name, mimetype="audio/mp3")
    
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
        print(f'GPT TEXT response: {response_text}')
        print("*"*40)
        
        return jsonify(response_text)
    
class DalleClothes(Resource):
    def get(self):
        return jsonify({"message": "Response DALLE IMAGE post a text"})
    
    def post(self):
        clothestext = request.get_json()['clothestext']
        
        print(f'Wanted Clothes Text : {clothestext}')
        response = openai.Image.create(
            prompt=clothestext,
            n=1,
            size="256x256"
        )
        image_url = response['data'][0]['url']
        file_name = f'images/dll_img_{hash(image_url)}.png'
        
        res = requests.get(image_url, stream = True)
        
        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ', file_name)
            return send_file(file_name, mimetype='image/png')
        else:
            print('Image Couldn\'t be retrieved')
            return jsonify({"error": "Image Couldn\'t be retrieved"})

    
api.add_resource(Rasa, '/rasachat')
api.add_resource(RasaVoice, '/rasavoice')
api.add_resource(GptText, '/gpttext')
api.add_resource(DalleClothes, '/dalleimggen')

    
if __name__ == '__main__':
    app.run(debug=True)
        