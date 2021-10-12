from flask import Blueprint,request,flash,jsonify
from flask.helpers import url_for
from flask import render_template
from flask_login import login_required,current_user
from .models import Note
from . import db
from datetime import datetime
import json

views = Blueprint('views', __name__)

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

    return render_template('home.html', user=current_user)


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