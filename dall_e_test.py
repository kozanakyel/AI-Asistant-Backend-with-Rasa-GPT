from dotenv import load_dotenv
import os
import openai
import requests
import shutil

load_dotenv()

CHATGPT_ENV=os.getenv('CHATGPT')

openai.api_key = CHATGPT_ENV

response = openai.Image.create(
  prompt="a yellow tshirt with small L char logo and text with life is dream",
  n=1,
  size="256x256"
)
image_url = response['data'][0]['url']

file_name = 'images/dalle_image_skirt.png'

res = requests.get(image_url, stream = True)

if res.status_code == 200:
    with open(file_name,'wb') as f:
        shutil.copyfileobj(res.raw, f)
    print('Image sucessfully Downloaded: ', file_name)
else:
    print('Image Couldn\'t be retrieved')
print(image_url)
