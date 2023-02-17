import requests, os
from dotenv import load_dotenv
load_dotenv()

LOGIN_BOT = os.getenv('LOGIN_BOT_TOKEN')

url_info = f"https://api.telegram.org/bot{LOGIN_BOT}/getUpdates"
result = requests.get(url=url_info).json()

print(result)