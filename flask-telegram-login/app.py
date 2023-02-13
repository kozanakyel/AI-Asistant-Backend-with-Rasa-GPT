from flask import Flask, render_template, request,jsonify,redirect, session
import json
import hashlib
import hmac
import base64
from dotenv import load_dotenv
import os

load_dotenv()

LOGIN_BOT_TOKEN = os.getenv('LOGIN_BOT_TOKEN')

app = Flask(__name__)

app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']




@app.route('/')
def index():
	data = {'bot_name': app.config['BOT_NAME'], 'bot_domain': app.config['BOT_DOMAIN']}
	print(f'data for bot: {data}')
	return render_template('index.html',data = data)

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

def string_generator(data_incoming):
	print(f'data incoming string genarator: {data_incoming}')
	data = data_incoming.copy()
	del data['hash']
	keys = sorted(data.keys())
	string_arr = []
	for key in keys:
		print(f"key: {key}")
		if data[key] != None:
			#data[key] = ''
			string_arr.append(key+'='+data[key])
	string_cat = '\n'.join(string_arr)
	return string_cat

@app.route('/login')
def login():
	tg_data = {
		"id" : request.args.get('id',None),
		"first_name" : request.args.get('first_name',None),
		"last_name" : request.args.get('last_name', None),
		"username" : request.args.get('username', None),
		"photo_url" : request.args.get('photo_url', None),
		"auth_date":  request.args.get('auth_date', None),
		"hash" : request.args.get('hash', None)
	}
	print(f'data login in first: {tg_data}')
	data_check_string = string_generator(tg_data)
	secret_key = hashlib.sha256(LOGIN_BOT_TOKEN.encode('utf-8')).digest()
	secret_key_bytes = secret_key
	data_check_string_bytes = bytes(data_check_string,'utf-8')
	hmac_string = hmac.new(secret_key_bytes, data_check_string_bytes, hashlib.sha256).hexdigest()
	if hmac_string == tg_data['hash']:
		return redirect('/dashboard')
	
	return jsonify({
				'hmac_string': hmac_string,
				'tg_hash': tg_data['hash'],
				'tg_data': tg_data
	})


if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True, port=8080)