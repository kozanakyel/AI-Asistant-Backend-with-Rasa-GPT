from flask import Flask, request, session
from flask_cors import CORS
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room
from flask_socketio import close_room, rooms, disconnect
from threading import Lock

#NAsil Calisir
"""
activate venv
pip install flask, flask-socketio, flask-cors
python app_denem_socket.py
"""

#Ayrica Socket nasil calisir backend cok kisa aciklama okunabilir
#https://flask-socketio.readthedocs.io/en/latest/getting_started.html

app = Flask(__name__)
CORS(app)

async_mode = None

socketio = SocketIO(app, async_mode=async_mode,  cors_allowed_origins="*")

thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


class MyNamespace(Namespace):
    def on_my_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']})

    def on_my_broadcast_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']},
             broadcast=True)

    def on_join(self, message):
        join_room(message['room'])
        print(f'room no: {message["room"]}')
        session['receive_count'] = session.get('receive_count', 0) + 1
        with open('OSR_us_000_0010_8k.wav', 'rb') as f:
            audio_binary = f.read()
        #emit('audio', {'data': audio_binary})
        emit('my_response',
             {'data': audio_binary,
              'count': session['receive_count']})

    def on_leave(self, message):
        leave_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'In rooms: ' + ', '.join(rooms()),
              'count': session['receive_count']})

    def on_close_room(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                             'count': session['receive_count']},
             room=message['room'])
        close_room(message['room'])

    def on_my_room_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']},
             room=message['room'])

    def on_disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()

    def on_my_ping(self):
        emit('my_pong')

    def on_connect(self):
        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(background_thread)
        emit('my_response', {'data': 'Connected', 'count': 0})

    def on_disconnect(self):
        print('Client disconnected', request.sid)

socketio.on_namespace(MyNamespace('/socket'))

    
if __name__ == '__main__':
    app.run(debug=True)
        