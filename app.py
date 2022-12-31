import os
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, send, leave_room

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


@socketio.on('leave')
def handle_leave(data):
    data = eval(data)
    leave_room(data.get('room'))
    room = data.get('room')
    return_string = '{"message": "' + data.get('username') + ' has left the room","username": "Server"}'
    emit('message', return_string, room=room)


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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    print('Running on port ' + str(port))
    socketio.run(app, debug=True, port=port, host='0.0.0.0')
