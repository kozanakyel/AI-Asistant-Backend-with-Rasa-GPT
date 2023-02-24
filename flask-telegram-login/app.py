from flask import Flask, render_template, request,jsonify,redirect, session
import json
import hashlib
import hmac
import base64
from dotenv import load_dotenv
import os
from functools import wraps

load_dotenv()

LOGIN_BOT_TOKEN = os.getenv('LOGIN_BOT_TOKEN')

app = Flask(__name__)

app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']


def telegram_auth_required(func):
	def wrapper(*args, **kwargs):
		if 'telegram_data' in session:
			tg_data = session.get('telegram_data', {})
		else:
			tg_data = {
				"id" : request.args.get('id',None),
				"first_name" : request.args.get('first_name',None),
				"last_name" : request.args.get('last_name', None),
				"username" : request.args.get('username', None),
				"photo_url" : request.args.get('photo_url', None),
				"auth_date":  request.args.get('auth_date', None),
				"hash" : request.args.get('hash', None)
			}
		check_user_hash, _ = check_hmac_for_user_auth(telegram_data=tg_data, login_bot_token=LOGIN_BOT_TOKEN)
		if not check_user_hash:
			return jsonify({'error': 'unauthorized'})

		#session['telegram_data'] = tg_data
		return func(*args, **kwargs)

	return wrapper

@app.route('/index')
def index():
	data = {'bot_name': app.config['BOT_NAME'], 'bot_domain': app.config['BOT_DOMAIN']}
	#print(f'data for bot: {data}')
	return render_template('index.html', data = data)

def string_generator(data_incoming):
	#print(f'data incoming string genarator: {data_incoming}')
	data = data_incoming.copy()
	del data['hash']
	keys = sorted(data.keys())
	string_arr = []
	for key in keys:
		print(f"key: {key}")
		if data[key] != None:
			string_arr.append(key+'='+data[key])
	string_cat = '\n'.join(string_arr)
	return string_cat

def check_hmac_for_user_auth(telegram_data: dict, login_bot_token: str) -> bool:
	data_check_string = string_generator(telegram_data)
	secret_key = hashlib.sha256(login_bot_token.encode('utf-8')).digest()
	secret_key_bytes = secret_key
	data_check_string_bytes = bytes(data_check_string, 'utf-8')
	hmac_string = hmac.new(secret_key_bytes, data_check_string_bytes, hashlib.sha256).hexdigest()	
	return hmac_string == telegram_data["hash"], hmac_string

@app.route('/dashboard')
@telegram_auth_required
def dashboard():
    telegram_data = session.get('telegram_data', {})
    #print(telegram_data)
    return render_template('dashboard.html', telegram_data=telegram_data)

@app.route('/login')
def login():
    if 'telegram_data' in session:
        tg_data = session.get('telegram_data', {})
    else:
        tg_data = {
			"id" : request.args.get('id',None),
			"first_name" : request.args.get('first_name',None),
			"last_name" : request.args.get('last_name', None),
			"username" : request.args.get('username', None),
			"photo_url" : request.args.get('photo_url', None),
			"auth_date":  request.args.get('auth_date', None),
			"hash" : request.args.get('hash', None)
		}
    check_user_hash, hmac_string = check_hmac_for_user_auth(telegram_data=tg_data, login_bot_token=LOGIN_BOT_TOKEN)
    if check_user_hash:
        session['telegram_data'] = tg_data
        return redirect('/dashboard')
    
    return jsonify({
				'hmac_string': hmac_string,
				'tg_hash': tg_data['hash'],
				'tg_data': tg_data
	})
 
@app.route('/logout')
def logout():
    if 'telegram_data' in session:  
        session.pop('telegram_data', None)
    return redirect('/')


if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True, port=8080)