from flask import Flask, request, jsonify, make_response 
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import openai
from telegram import Bot
import asyncio
import requests
from gtts import gTTS
from io import BytesIO

load_dotenv()

app = Flask(__name__)

PSQL_USER_ENV=os.getenv('PSQL_USER')
PSQL_PWD_ENV=os.getenv('PSQL_PWD')
PSQL_URI_ENV=os.getenv('PSQL_URI')
PSQL_PORT_ENV=os.getenv('PSQL_PORT')
PSQL_DB_NAME_ENV=os.getenv('PSQL_DB_NAME')

CHATGPT_ENV=os.getenv('CHATGPT')

TELEGRAM_BOT_API_ENV = os.getenv('TELEGRAM_BOT_API')

CHAT_ID = os.getenv('CHAT_ID_GROUP')

openai.api_key = CHATGPT_ENV
bot = Bot(TELEGRAM_BOT_API_ENV)

async def send_telegram_message(bot, chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_ENV}/sendMessage?chat_id={chat_id}&text={message}"
    #await bot.send_message(chat_id=chat_id, text=message)
    await requests.get(url).json()
    
async def send_audio_telegram_message(bot, chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_ENV}/sendAudio"
    #await bot.send_message(chat_id=chat_id, text=message)
    parameters = {
        "chat_id": chat_id,
        "audio": "response.mp3",
        "caption": "response audio received"
    }
    await requests.get(url, data=parameters).json()
    
def send_audio_with_telegram(chat_id: str, file_path: str, post_file_title: str, bot_token: str) -> None:
    with open(file_path, 'rb') as audio:
        payload = {
            'chat_id': chat_id,
            'title': post_file_title,
            'parse_mode': 'HTML'
        }
        files = {
            'audio': audio.read(),
        }
        resp = requests.post(
            "https://api.telegram.org/bot{token}/sendAudio".format(token=bot_token),
            data=payload,
            files=files).json()

@app.route('/question', methods=['POST'])
async def question():
    data = request.get_json()
    question = data['question']
    print(f'Question : {question}')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=256,
        n=1
    )
    response_text = response['choices'][0]['text']
    print(f'Response : {response_text}') 
    tts = gTTS(response_text, lang='tr', tld="com")
    tts.save(f'resp-{response_text[:5]}.mp3')
    send_audio_with_telegram(chat_id=CHAT_ID,
                             file_path=f'resp-{response_text[:5]}.mp3',
                             post_file_title=f'received-{response_text[:5]}.mp3',
                             bot_token=TELEGRAM_BOT_API_ENV)
    #audio_file = BytesIO()
    #tts.write_to_fp(audio_file)
    #asyncio.ensure_future(send_audio_telegram_message(bot=bot,
    #                                            chat_id='1678406668',
    #                                            message=response_text))
    #bot.send_message(chat_id='756050439', text=response_text)
    return response_text

if __name__ == '__main__':
    app.run(debug=True)