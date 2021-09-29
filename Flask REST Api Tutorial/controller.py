from datetime import datetime
from flask import Flask,jsonify,request,render_template
from flask_restful import Api, Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy
import socketio
from flask_socketio import SocketIO,send,emit
from models import db,VideoModel,Note,User,Channel,Team

class _Resources():
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'views': fields.Integer,
        'likes': fields.Integer,
    }
    user_fields = {
        'id': fields.Integer,
        'first_name': fields.String,
        'email': fields.String,
        'notes': fields.List,
        'channels':fields.List
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
    }
    team_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'user_id': fields.Integer
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
            note_add_args.add_argument("data", type=str, help="Name of the video is required",required=True)
            note_add_args.add_argument("date", type=datetime)
            note_add_args.add_argument("user_id", type=int, help="Likes of the video is required",required=True)
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
            user_add_args.add_argument("name", type=str, help="Name of the video is required",required=True)
            user_add_args.add_argument("views", type=int, help="Views of the video is required",required=True)
            user_add_args.add_argument("likes", type=int, help="Likes of the video is required",required=True)
            return user_add_args
        elif(add_or_update == 2):
            user_update_args = reqparse.RequestParser()
            user_update_args.add_argument("name", type=str)
            user_update_args.add_argument("views", type=int)
            user_update_args.add_argument("likes", type=int)
            return user_update_args
    
    def channel(add_or_update:int):
        if(add_or_update == 1):
            channel_add_args = reqparse.RequestParser()
            channel_add_args.add_argument("name", type=str, help="Name of the video is required",required=True)
            channel_add_args.add_argument("views", type=int, help="Views of the video is required",required=True)
            channel_add_args.add_argument("likes", type=int, help="Likes of the video is required",required=True)
            return channel_add_args
        elif(add_or_update == 2):
            channel_update_args = reqparse.RequestParser()
            channel_update_args.add_argument("name", type=str)
            channel_update_args.add_argument("views", type=int)
            channel_update_args.add_argument("likes", type=int)
            return channel_update_args

    def team(add_or_update:int):
        if(add_or_update == 1):
            team_add_args = reqparse.RequestParser()
            team_add_args.add_argument("name", type=str, help="Name of the video is required",required=True)
            team_add_args.add_argument("views", type=int, help="Views of the video is required",required=True)
            team_add_args.add_argument("likes", type=int, help="Likes of the video is required",required=True)
            return team_add_args
        elif(add_or_update == 2):
            team_update_args = reqparse.RequestParser()
            team_update_args.add_argument("name", type=str)
            team_update_args.add_argument("views", type=int)
            team_update_args.add_argument("likes", type=int)
            return team_update_args

class UserById(Resource):
    @marshal_with(_Resources.user_fields)
    def get(self,user_id):
        if(user_id):
            result = User.query.filter_by(id = user_id).first()
        if not result:
            abort(404, message = f"Could not find user with {user_id}")
        return result,200
    
    #This is used for adding a user
    @marshal_with(_Resources.user_fields)
    def put(self,user_id):
        args = add_update_args.user(1).parse_args()

        result = VideoModel.query.filter_by(id=user_id).first()
        if result:
            abort(409, message="video id taken...")

        video = VideoModel(id=user_id,email=args['email'], password = args[''],likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(_Resources.user_fields)
    def patch(self,video_id):
        args = add_update_args.user(2).parse_args()

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


class VideoById(Resource):
    @marshal_with(_Resources.resource_fields)
    def get(self,video_id):
        if(video_id):
            result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message=f"Could not find video with {video_id}")
        return result, 200
    
    @marshal_with(_Resources.resource_fields)
    def put(self,video_id):
        args = add_update_args.video(1).parse_args()

        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="video id taken...")

        video = VideoModel(id=video_id,name=args['name'], views = args['views'],likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(_Resources.resource_fields)
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

    @marshal_with(_Resources.resource_fields)
    def get(self):
        result = VideoModel.query.all()
            
        if not result:
            abort(404, message="Could not find any videos")
        return result, 200

    @marshal_with(_Resources.resource_fields)
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