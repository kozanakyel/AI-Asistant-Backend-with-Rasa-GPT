from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.rasa_text import RasaText
from resources.rasa_voice import RasaVoice
from resources.gpt_text import GptText
from resources.dall_e_clothes import DalleClothes

app = Flask(__name__)
CORS(app)
api = Api(app)
   
api.add_resource(RasaText, '/rasatext')
api.add_resource(RasaVoice, '/rasavoice')
api.add_resource(GptText, '/gpttext')
api.add_resource(DalleClothes, '/dalleimggen')

    
if __name__ == '__main__':
    app.run(debug=True)
        