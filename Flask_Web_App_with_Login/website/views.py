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
async_type = "eventlet"

sio = SocketIO(async_type = async_type)
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
    myNotes = Note.query.all()
    return render_template('home.html',allNotes=myNotes,user=current_user,async_mode = sio.async_mode)

@sio.event
def my_event(message):
    pass
    #emit('my_response',{'data': message['data']})

@sio.event
def getUser():
    emit('c_user',{'data': current_user.id})

@sio.event
def my_broadcast_event(message):
    #session['receive_count'] = session.get('receive_count', 0) + 1
    new_note = Note(data=message['data'], date = datetime.now(),user_id = current_user.id)
    db.session.add(new_note)
    db.session.commit()
    edit = """
    <div id = "edDel">
        <div type = "button" id = "editB">
            <img src="./static/images/edit.png" id = "editImage" onclick = "editNote('{{note.id}}')">
        </div>
        &nbsp;
        <button type="button" class="btn-close" id = "closeX" aria-label="Close" onclick="deleteNote('{{note.id}}')"></button>
    </div>
    """
    emit('message_add',{'user_name': f"{current_user.first_name}",'data':  f"{new_note.data}", 'id': f"{new_note.user_id}", 'edit':edit} ,broadcast=True)

@sio.event
def edit_event(message):
    if(message['data']):
        
        pass
        #session['receive_count'] = session.get('receive_count', 0) + 1
        #emit('my_response',{'data':  f"{current_user.first_name} : {new_note.data}"},broadcast=True)

@sio.event
def delete_event(message):
    #session['receive_count'] = session.get('receive_count', 0) + 1
    if(message['data']):
        pass
        #emit('my_response',{'data':  f"{current_user.first_name} : {new_note.data}"},broadcast=True)
    
@sio.event
def load_all_messages():
    results = Note.query.all()
    
    #print(edit)
    #for result in results:
    #    emit("saved_messages", {'data': result.data, 'note_id': result.id, 'user_id':result.user_id, 'note_date':result.date})

"""
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
"""
@sio.event
def my_ping():
    emit('my_pong')

@sio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = sio.start_background_task(background_thread)
    print(f"{current_user.first_name} connected")
    
@sio.event
def disconnect():
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

@views.route('/edit-note', methods=['GET','POST'])
@login_required
def editNote():
    note = json.loads(request.data)
    print(f"{note['noteId']}: {note['note_data']}")
    noteId = note['noteId']
    note_data = note['note_data']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            if note_data:
                note.data = note_data
            db.session.commit()
    
    return jsonify({})