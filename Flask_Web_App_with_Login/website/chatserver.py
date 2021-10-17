from flask_socketio import SocketIO,send,emit,join_room,leave_room,close_room,rooms,disconnect
from flask import request
from flask_login import current_user,login_required
from threading import Lock
from flask import copy_current_request_context,session

#async_mode= None

#socketio = SocketIO(async_mode = async_mode)

"""
@socketio.on('connect')
def connect_handler():
    if current_user.is_authenticated:
        print(f"{current_user.first_name} Connected")
        emit('my response',
             {'message': f"Welcome to chat {current_user.first_name}"})
    else:
        return False  # not allowed here

@socketio.on('disconnect')
def test_disconnect():
    emit('my response',
             {'message': f"{current_user.first_name} disconnected"})
    print(f"{current_user.first_name} Disconnected")

@socketio.on('message')
def handle_message(message):
    send(message)
    print(f'received message: {message}')

@socketio.on('json')
def handle_json(json):
    send(json, json=True)

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)

@socketio.on("my error event")
def on_my_event(data):
    raise RuntimeError()

@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"]) # "my error event"
    print(request.event["args"])    # (data,)

"""