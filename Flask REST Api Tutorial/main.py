from flask import Flask,jsonify,request,render_template
from flask_restful import Api, Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO,send,emit
from controller import db,GetAllVideos,VideoById,UserById,GetAllUsers,TeamById,GetAllTeams,ChannelById,GetAllChannels,NoteById,GetAllNotes
from os import path

DATABASE_NAME = "ChatDatabase.db"

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'BestEverPassword'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

if not(path.exists(DATABASE_NAME)):
    db.create_all(app = app)

#socketio = SocketIO(app)

api.add_resource(GetAllVideos,"/video")
api.add_resource(VideoById,"/video/<int:video_id>")
api.add_resource(UserById, "/user/<int:user_id>")
api.add_resource(GetAllUsers,"/user")
api.add_resource(NoteById, "/note/<int:note_id>")
api.add_resource(GetAllNotes,"/note")
api.add_resource(ChannelById, "/channel/<int:channel_id>")
api.add_resource(GetAllChannels,"/channel")
api.add_resource(TeamById, "/team/<int:team_id>")
api.add_resource(GetAllTeams,"/team")


if __name__ == "__main__":
    #socketio.run(app,host='localhost',port = 3000,debug=True)
    app.run(host='localhost',port = 3000,debug=True)