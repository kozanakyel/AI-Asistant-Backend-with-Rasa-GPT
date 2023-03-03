### SHOPYVERSE - RASA ASI-based chatbot - GPT bot 

This Program include Backend, Rasa chatbot and Gpt bot for both Telegram user group and Meatverse integration.
For the first step and runnig locally documentation

## Steps for local run

you can define openai api key in .env file

cd  .../{project-folder}

python3 -m venv venv

source venv/bin/activate   =>for linux and wsl2

./venv/bin/activate.ps     =>for windows

pip install -r requirements.txt    =>for first run

python3 -m spacy download en_core_web_md   =>for first run

cd .../backend-shopyverse 

python app.py

cd .../rasa_chatbot 

rasa run actions

rasa run --enable-api


