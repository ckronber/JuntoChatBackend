from flask import Flask
from flask_socketio import send,SocketIO,emit

socketio = SocketIO()

@socketio.on('message')
def handleMessage(msg):
    print('Message:'+ msg)
    send(msg)