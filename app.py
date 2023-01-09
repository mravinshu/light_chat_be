import datetime
import os
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, send, leave_room
import redis

redis = redis.Redis(host='singapore-redis.render.com', port=6379, db=0, password='DAe95s9HP2CTSrgheLMDdkfuaoGc10a8',
                    username='red-ceu2v3pa6gdut0r7ca50', ssl=True)

# redis = redis.Redis(host='localhost', port=6379, db=0, password='r')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'RandomSecretKey'
socketio = SocketIO(app, cors_allowed_origins="*", logging=True, engineio_logger=True)


@app.route('/')
def index():
    return {'message': 'Hello World'}


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('message', message)


@socketio.on('message_to')
def handle_message_to(message):
    message = eval(message)
    print('received message: ' + str(message))
    returnString = '{"message": "' + message.get('message') + '","username": "' + message.get('username') + '"}'
    print(returnString)
    emit('message', returnString, room=message.get('room'), include_self=False)
    returnString = eval(returnString)
    # Date and time of message
    returnString['time'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Save message to redis
    redis.lpush(message.get('room'), str(returnString))


@socketio.on('leave')
def handle_leave(data):
    data = eval(data)
    leave_room(data.get('room'))
    room = data.get('room')
    return_string = '{"message": "' + data.get('username') + ' has left the room","username": "Server"}'
    emit('message', return_string, room=room, include_self=False)
    returnString = eval(return_string)
    # Date and time of message
    returnString['time'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Save message to redis
    redis.lpush(data.get('room'), str(returnString))


@socketio.on('join')
def on_join(data):
    data = eval(data)
    username = data.get('username')
    room = data.get('room')
    join_room(room)
    print('user ' + username + ' joined room ' + room)
    returnString = '{"message": "' + 'user ' + username + ' joined room ' + room + '","username": "Server"}'
    # emit('my response', {'data': 'In rooms: ' + ', '.join(rooms())}, room=room)
    send(returnString, room=room, include_self=False)
    returnString = eval(returnString)
    # Date and time of message
    returnString['time'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Save message to redis
    redis.lpush(data.get('room'), str(returnString))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    print('Running on port ' + str(port))
    socketio.run(app, debug=True, port=port, host='0.0.0.0')
