from flask import Blueprint, config,request,flash,jsonify,copy_current_request_context,session,render_template
from flask_socketio import SocketIO,send,emit,join_room,leave_room,close_room,rooms,disconnect
from flask.helpers import url_for
from flask_login import login_required,current_user
from .models import Note
from . import db
from threading import Lock
from datetime import datetime
import json
from engineio.payload import Payload

views = Blueprint('views', __name__)
async_mode = 'gevent'
Payload.max_decode_packets = 500

socketio = SocketIO(async_mode = async_mode,ping_timeout=3,ping_interval=1)
thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    #while True:
    #    socketio.sleep(10)
    #    emit('my_response', {'data': 'Server generated event'})

"""
@views.route('/',methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Message is too short!', category='error')
        else:
            new_note = Note(data=note, date = datetime.now(),user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()

        return render_template('home.html', user=current_user, async_mode = socketio.async_mode)
"""

@views.route('/') #,methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user=current_user,async_mode = socketio.async_mode)

@socketio.event
def my_event(message):
    emit('my_response',
         {'data': message['data']})

@socketio.event
def my_broadcast_event(message):
    emit('my_response',
         {'data': f"{current_user.first_name} : " + message['data']},
         broadcast=True)

@socketio.event
def join(message):
    join_room(message['room'])
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})

@socketio.event
def leave(message):
    leave_room(message['room'])
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})

@socketio.on('close_room')
def on_close_room(message):
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.'},
         to=message['room'])
    close_room(message['room'])

@socketio.event
def my_room_event(message):
    emit('my_response',
         {'data': message['data']},
         to=message['room'])

@socketio.event
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!'},
         callback=can_disconnect)

@socketio.event
def my_ping():
    emit('my_pong')

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    #emit('my_response', {'data': 'Connected'})
    print(f"{current_user.first_name} connected")
    
@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)

@views.route('/delete-note', methods=['POST'])
@login_required
def deletenote():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/edit-note', methods=['POST','GET'])
@login_required
def editNote():
    note = json.loads(request.data)
    noteId = note['noteId']
    note_data = note['note_data']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            if note_data:
                note.data = note_data
            db.session.commit()
    
    return jsonify({})