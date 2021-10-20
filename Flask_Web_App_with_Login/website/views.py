from flask import Blueprint,config,request,flash,jsonify,copy_current_request_context,session,render_template
from flask_socketio import SocketIO,send,emit,join_room,leave_room,close_room,rooms,disconnect
from flask.helpers import url_for
from flask_login import login_required,current_user
from .models import Note
from . import db
from threading import Lock
from datetime import datetime
import json

views = Blueprint('views', __name__)

async_type = None

sio = SocketIO(async_type = async_type)
#,ping_timeout=3,ping_interval=1
thread = None
thread_lock = Lock()


def background_thread():
    """Example of how to send server generated events to clients."""
    print("background Thread")
    #while True:
    #    sio.sleep(10)
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

        return render_template('home.html', user=current_user, async_mode = sio.async_mode)
"""

@views.route('/') #,methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user=current_user,async_mode = sio.async_mode)

@sio.event
def my_event(message):
    emit('my_response',{'data': message['data']})

@sio.event
def my_broadcast_event(message):
    #if(message['data']):
        #session['receive_count'] = session.get('receive_count', 0) + 1
    new_note = Note(data=message['data'], date = datetime.now(),user_id = current_user.id)
    db.session.add(new_note)
    db.session.commit()
    emit('my_response',{'user_name': f"{current_user.first_name}",'data':  f"{new_note.data}"},broadcast=True)

@sio.event
def edit_event(message):
    if(message['data']):
        pass
        #session['receive_count'] = session.get('receive_count', 0) + 1
        #emit('my_response',{'data':  f"{current_user.first_name} : {new_note.data}"},broadcast=True)

@sio.event
def delete_event(message):
    if(message['data']):
        pass
        #session['receive_count'] = session.get('receive_count', 0) + 1
        #emit('my_response',{'data':  f"{current_user.first_name} : {new_note.data}"},broadcast=True)
    
@sio.event
def load_all_messages():
    results = Note.query.all()
    return results

@sio.event
def join(message):
    join_room(message['room'])
    emit('my_response', {'data': 'In rooms: ' + ', '.join(rooms())})

@sio.event
def leave(message):
    leave_room(message['room'])
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})

@sio.on('close_room')
def on_close_room(message):
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.'},
         to=message['room'])
    close_room(message['room'])

@sio.event
def my_room_event(message):
    emit('my_response',
         {'data': message['data']},
         to=message['room'])

@sio.event
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


@sio.event
def my_ping():
    emit('my_pong')

@sio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = sio.start_background_task(background_thread)
    #emit('my_response', {'data': 'Connected'})
    print(f"{current_user.first_name} connected")
    
@sio.on('disconnect')
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