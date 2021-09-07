import flask
from flask import url_for,abort,redirect,Flask,jsonify,make_response
from socketio import Server,WSGIApp,AsyncServer,ASGIApp
import os

sio = Server()
app = WSGIApp(sio)

@sio.event()
def my_event(sid, data):
    # handle the message
    return "OK", 123
#print(os.urandom(16))

# new comment

'''
app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])

def index():
    abort(503)

@app.route('/login')
def login():
    abort(503)

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s Profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login',next='/'))
    print(url_for('profile', username='ckronber'))

app.run()
'''