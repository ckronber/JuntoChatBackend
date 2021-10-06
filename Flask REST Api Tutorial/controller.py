from datetime import datetime
#from flask import Flask,jsonify,request,render_template
from flask_restful import Api, Resource,reqparse,abort,fields,marshal_with
#from flask_sqlalchemy import SQLAlchemy
from models import db,VideoModel,Note,User,Channel,Team

class Resources():
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'views': fields.Integer,
        'likes': fields.Integer,
    }
    user_fields = {
        'id': fields.Integer,
        'user_name': fields.String,
        'email': fields.String,
        'password':fields.String,
        'notes': fields.List,
        'channels':fields.List,
        'teams':fields.List
    }
    note_fields = {
        'id': fields.Integer,
        'data': fields.String,
        'date': fields.DateTime,
        'user_id': fields.Integer,
    }
    channel_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'user_id': fields.Integer,
        'channel_users':fields.List
    }
    team_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'user_id': fields.Integer,
        'team_users':fields.List
    }
    team_user_fields = {
        'id': fields.Integer,
        'user_name': fields.String,
        'team_id': fields.Integer
    }
    channel_user_fields = {
        'id': fields.Integer,
        'user_name': fields.String,
        'channel_id': fields.Integer
    }

class add_update_args():
    def video(add_or_update:int):
        if(add_or_update == 1):
            video_add_args = reqparse.RequestParser()
            video_add_args.add_argument("name", type=str, help="Name of the video is required",required=True)
            video_add_args.add_argument("views", type=int, help="Views of the video is required",required=True)
            video_add_args.add_argument("likes", type=int, help="Likes of the video is required",required=True)
            return video_add_args

        elif(add_or_update == 2):
            video_update_args = reqparse.RequestParser()
            video_update_args.add_argument("name", type=str)
            video_update_args.add_argument("views", type=int)
            video_update_args.add_argument("likes", type=int)
            return video_update_args

    def note(add_or_update:int):
        if(add_or_update == 1):
            note_add_args = reqparse.RequestParser()
            note_add_args.add_argument("data", type=str, help="data is required",required=True)
            note_add_args.add_argument("date", type=datetime)
            note_add_args.add_argument("user_id", type=int, help="user_id is required",required=True)
            return note_add_args
        elif(add_or_update == 2):
            note_update_args = reqparse.RequestParser()
            note_update_args.add_argument("data", type=str)
            note_update_args.add_argument("date", type=datetime)
            note_update_args.add_argument("user_id", type=int)
            return note_update_args

    def user(add_or_update:int):
        if(add_or_update == 1):
            user_add_args = reqparse.RequestParser()
            user_add_args.add_argument("user_name", type=str, help="Username is required",required=True)
            user_add_args.add_argument("email", type=str, help="email is required",required=True)
            user_add_args.add_argument("password", type=str, help="password is required",required=True)
            return user_add_args

        elif(add_or_update == 2):
            user_update_args = reqparse.RequestParser()
            user_update_args.add_argument("user_name", type=str)
            user_update_args.add_argument("email", type=str)
            user_update_args.add_argument("password", type=str)
            return user_update_args
    
    def channel(add_or_update:int):
        if(add_or_update == 1):
            channel_add_args = reqparse.RequestParser()
            channel_add_args.add_argument("name", type=str, help="Name of the channel is required",required=True)
            channel_add_args.add_argument("descrioption", type=str, help="Description is required",required=True)
            channel_add_args.add_argument("user_id", type=int, help="user_id is required",required=True)
            return channel_add_args
        elif(add_or_update == 2):
            channel_update_args = reqparse.RequestParser()
            channel_update_args.add_argument("name", type=str)
            channel_update_args.add_argument("description", type=str)
            channel_update_args.add_argument("user_id", type=int)
            return channel_update_args

    def team(add_or_update:int):
        if(add_or_update == 1):
            team_add_args = reqparse.RequestParser()
            team_add_args.add_argument("name", type=str, help="Name of the video is required",required=True)
            team_add_args.add_argument("user_id", type=int, help="Views of the video is required",required=True)
            return team_add_args
        elif(add_or_update == 2):
            team_update_args = reqparse.RequestParser()
            team_update_args.add_argument("name", type=str)
            team_update_args.add_argument("user_id", type=int)
            return team_update_args

    def team_users(add_or_update:int):
        if(add_or_update == 1):
            team_user_add_args = reqparse.RequestParser()
            team_user_add_args.add_argument("user_name", type=str, help="username is required",required=True)
            team_user_add_args.add_argument("team_id", type=int, help="team_id is required",required=True)
            return team_user_add_args

        elif(add_or_update == 2):
            team_user_update_args = reqparse.RequestParser()
            team_user_update_args.add_argument("user_name", type=str)
            team_user_update_args.add_argument("team_id", type=int)
            return team_user_update_args
    
    def channel_users(add_or_update:int):
        if(add_or_update == 1):
            team_user_add_args = reqparse.RequestParser()
            team_user_add_args.add_argument("name", type=str, help="username is required",required=True)
            team_user_add_args.add_argument("channel_id", type=int, help="channel_id is required",required=True)
            return team_user_add_args

        elif(add_or_update == 2):
            team_user_update_args = reqparse.RequestParser()
            team_user_update_args.add_argument("user_name", type=str)
            team_user_update_args.add_argument("channel_id", type=int)
            return team_user_update_args

class UserById(Resource):
    @marshal_with(Resources.user_fields)
    def get(self,user_id):
        if(user_id):
            result = User.query.filter_by(id = user_id).first()
        if not result:
            abort(404, message = f"Could not find user with {user_id}")
        return result,200
    
    #This is used for adding a user
    @marshal_with(Resources.user_fields)
    def put(self,user_id):
        args = add_update_args.user(1).parse_args()

        result = User.query.filter_by(id=user_id).first()
        if result:
            abort(409, message="user id taken...")

        user = User(id=user_id,email=args['email'], password = args['password'],user_name = args['user_name'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(Resources.user_fields)
    def patch(self,video_id):
        args = add_update_args.user(2).parse_args()

        result = User.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message = "User doesn't exist, cannot update")

        if args['user_name']:
            result.user_name = args['user_name']
        if args['email']:
            result.email = args['email']
        if args['password']:
            result.password = args['password']

        db.session.commit()
        return result, 201

    def delete(self,user_id):
        result = User.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Could not find video with that id")
        db.session.delete(result)
        db.session.commit()
        return 'Deleted', 204

class GetAllUsers(Resource):

    @marshal_with(Resources.user_fields)
    def get(self):
        result = User.query.all()
            
        if not result:
            abort(404, message="Could not find any videos")
        return result, 200

    @marshal_with(Resources.user_fields)
    def post(self):     
        args = add_update_args.user(1).parse_args()
        
        result = User.query.all()

        if result:
            result = result[-1].id
            user = User(id=result+1,user_name= args['user_name'], email = args['email'],password = args['password'])
        if not result:
            user = User(id=1, user_name = args['user_name'], email = args['email'], password = args['password'])
    
        db.session.add(user)
        db.session.commit()

        return user,201

class NoteById(Resource):
    @marshal_with(Resources.note_fields)
    def get(self,note_id):
        if(note_id):
            result = Note.query.filter_by(id = note_id).first()
        if not result:
            abort(404, message = f"Could not find user with {note_id}")
        return result,200

    
        
    #This is used for adding a user
    @marshal_with(Resources.note_fields)
    def put(self,note_id):
        args = add_update_args.note(1).parse_args()

        result = User.query.filter_by(id=note_id).first()
        if result:
            abort(409, message="note id taken...")

        note = Note(id=note_id,data=args['data'], user_id = args['user_id'])
        db.session.add(note)
        db.session.commit()
        return note, 201

    @marshal_with(Resources.note_fields)
    def patch(self,note_id):
        args = add_update_args.note(2).parse_args()

        result = Note.query.filter_by(id=note_id).first()
        if not result:
            abort(404, message = "Note doesn't exist, cannot update")

        if args['data']:
            result.data = args['data']
        if args['user_id']:
            result.user_id = args['user_id']

        db.session.commit()
        return result, 201

    def delete(self,note_id):
        result = Note.query.filter_by(id=note_id).first()
        if not result:
            abort(404, message="Could not find note with that id")
        db.session.delete(result)
        db.session.commit()
        return 'Deleted', 204

class GetAllNotes(Resource):
    @marshal_with(Resources.note_fields)
    def get(self):
        result = Note.query.all()
            
        if not result:
            abort(404, message="Could not find any notes")
        return result, 200

    @marshal_with(Resources.note_fields)
    def post(self):     
        args = add_update_args.note(1).parse_args()
        
        result = Note.query.all()

        if result:
            result = result[-1].id
            note = Note(id=result+1,data= args['data'], user_id = args['user_id'])
        if not result:
            note = Note(id=1, data= args['data'], user_id = args['user_id'])
    
        db.session.add(note)
        db.session.commit()

        return note,201

class ChannelById(Resource):
    @marshal_with(Resources.channel_fields)
    def get(self,channel_id):
        if(channel_id):
            result = Channel.query.filter_by(id = channel_id).first()
        if not result:
            abort(404, message = f"Could not find channel with {channel_id}")
        return result,200
    
    #This is used for adding a user
    @marshal_with(Resources.channel_fields)
    def put(self,channel_id):
        args = add_update_args.channel(1).parse_args()

        result = Channel.query.filter_by(id=channel_id).first()
        if result:
            abort(409, message="channel id taken...")

        channel = Channel(id=channel_id,name=args['name'],description=args['description'], user_id = args['user_id'])
        db.session.add(channel)
        db.session.commit()
        return channel, 201

    @marshal_with(Resources.channel_fields)
    def patch(self,channel_id):
        args = add_update_args.channel(2).parse_args()

        result = Channel.query.filter_by(id=channel_id).first()
        if not result:
            abort(404, message = "Channel doesn't exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['description']:
            result.description = args['description']
        if args['user_id']:
            result.user_id = args['user_id']

        db.session.commit()
        return result, 201

    def delete(self,channel_id):
        result = Channel.query.filter_by(id=channel_id).first()
        if not result:
            abort(404, message="Could not find channel with that id")
        db.session.delete(result)
        db.session.commit()
        return 'Deleted', 204

class GetAllChannels(Resource):
    @marshal_with(Resources.channel_fields)
    def get(self):
        result = Channel.query.all()
            
        if not result:
            abort(404, message="Could not find any notes")
        return result, 200

    @marshal_with(Resources.channel_fields)
    def post(self):     
        args = add_update_args.channel(1).parse_args()
        
        result = Channel.query.all()

        if result:
            result = result[-1].id
            channel = Channel(id=result+1,name= args['name'],description= args['description'],user_id = args['user_id'])
        if not result:
            channel = Channel(id=1, name= args['name'],description= args['description'],user_id = args['user_id'])
    
        db.session.add(channel)
        db.session.commit()

        return channel,201

class TeamById(Resource):
    @marshal_with(Resources.team_fields)
    def get(self,team_id):
        if(team_id):
            result = Team.query.filter_by(id = team_id).first()
        if not result:
            abort(404, message = f"Could not find team with {team_id}")
        return result,200
    
    #This is used for adding a user
    @marshal_with(Resources.team_fields)
    def put(self,team_id):
        args = add_update_args.team(1).parse_args()

        result = Team.query.filter_by(id=team_id).first()
        if result:
            abort(409, message="team id taken...")

        team = Team(id=team_id,name=args['name'],user_id = args['user_id'])
        db.session.add(team)
        db.session.commit()
        return team, 201

    @marshal_with(Resources.team_fields)
    def patch(self,team_id):
        args = add_update_args.team(2).parse_args()

        result = Team.query.filter_by(id=team_id).first()
        if not result:
            abort(404, message = "Team doesn't exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['user_id']:
            result.user_id = args['user_id']

        db.session.commit()
        return result, 201

    def delete(self,team_id):
        result = Team.query.filter_by(id=team_id).first()
        if not result:
            abort(404, message="Could not find team with that id")
        db.session.delete(result)
        db.session.commit()
        return 'Deleted', 204

class GetAllTeams(Resource):
    @marshal_with(Resources.team_fields)
    def get(self):
        result = Team.query.all()
            
        if not result:
            abort(404, message="Could not find any Teams")
        return result, 200

    @marshal_with(Resources.team_fields)
    def post(self):     
        args = add_update_args.team(1).parse_args()
        
        result = Team.query.all()

        if result:
            result = result[-1].id
            team = Team(id=result+1,name= args['name'],user_id = args['user_id'])
        if not result:
            team = Team(id=1, name= args['name'],user_id = args['user_id'])
    
        db.session.add(team)
        db.session.commit()

        return team,201

class VideoById(Resource):
    @marshal_with(Resources.resource_fields)
    def get(self,video_id):
        if(video_id):
            result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"Could not find video with {video_id}")
        return result, 200
    
    @marshal_with(Resources.resource_fields)
    def put(self,video_id):
        args = add_update_args.video(1).parse_args()

        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="video id taken...")

        video = VideoModel(id=video_id,name=args['name'], views = args['views'],likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(Resources.resource_fields)
    def patch(self,video_id):
        args = add_update_args.video(2).parse_args()

        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message = "Video doesn't exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        return result, 201

    def delete(self,video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with that id")
        db.session.delete(result)
        db.session.commit()
        return 'Deleted', 204

class GetAllVideos(Resource):

    @marshal_with(Resources.resource_fields)
    def get(self):
        result = VideoModel.query.all()
            
        if not result:
            abort(404, message="Could not find any videos")
        return result, 200

    @marshal_with(Resources.resource_fields)
    def post(self):     
        args = add_update_args.video(1).parse_args()
        
        result = VideoModel.query.all()

        if result:
            result = result[-1].id
            video = VideoModel(id=result+1,name= args['name'], views = args['views'],likes = args['likes'])
        if not result:
            video = VideoModel(id=1, name= args['name'], views = args['views'], likes = args['likes'])
    
        db.session.add(video)
        db.session.commit()

        return video,201