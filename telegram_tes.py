from dotenv import load_dotenv
import os
import openai
import asyncio
import requests
from gtts import gTTS
from io import BytesIO
import time

load_dotenv()

# /getme : bot status for all settings

CHATGPT_ENV=os.getenv('CHATGPT')

TELEGRAM_BOT_API_ENV = os.getenv('TELEGRAM_BOT_API')


openai.api_key = CHATGPT_ENV

TOKEN = os.getenv('TELEGRAM_BOT_API')
CHAT_ID_BOT = os.getenv('CHAT_ID_BOT')
CHAT_ID_GROUP = os.getenv('CHAT_ID_GROUP')
message = "deneme mesaji"

url_bot_message = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID_GROUP}&text={message}"

url_info = f"https://api.telegram.org/bot{TOKEN}/getUpdates"


def url_send_message(chat_id: str, message: str):
    return f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    
    
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

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def remove_spaces(string):
    return "".join(string.split())


last_textchat = (None, None)
while True:
    # ses klasoru icindekileri komple silmek gerekli
    result = requests.get(url=url_info).json()
    try:
        question, chat = get_last_chat_id_and_text(result)
        #print(f"text, chat  {text} {chat}")
        if (question, chat) != last_textchat and question[:3] == 'gpt':
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=question[2:],
                max_tokens=256,
                n=1
            )
            response_text = response['choices'][0]['text']
            print(f'Response : {response_text}') 
            tts = gTTS(response_text, lang='tr', tld="com")
            tts.save(f'audios/ChatGPT{remove_spaces(response_text[:5])}.mp3')
            send_audio_with_telegram(chat_id=CHAT_ID_GROUP,
                             file_path=f'audios/ChatGPT{remove_spaces(response_text[:5])}.mp3',
                             post_file_title=f'received-{remove_spaces(response_text[:5])}.mp3',
                             bot_token=TELEGRAM_BOT_API_ENV)
            #requests.get(url=url_send_message(chat, question)).json()
            last_textchat = (question, chat)
    except:
        print(f'last activity not including message')
    time.sleep(1)
    