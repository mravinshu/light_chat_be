from flask import Flask
from flask_socketio import SocketIO, emit, join_room, send, rooms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RandomSecretKey'
socketio = SocketIO(app, cors_allowed_origins="*")


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
    emit('message', message.get('message'), room=message.get('room'), include_self=False)


@socketio.on('join')
def on_join(data):
    data = eval(data)
    username = data.get('username')
    room = data.get('room')
    join_room(room)
    # emit('my response', {'data': 'In rooms: ' + ', '.join(rooms())}, room=room)
    send(username + ' has entered the room.', room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
