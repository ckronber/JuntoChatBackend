from flask import Flask,jsonify,request,render_template
from flask_restful import Api, Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy
import socketio
from sqlalchemy_utils.functions import database_exists
from flask_socketio import SocketIO,send,emit
from main import app
from . import db
'''
socket = SocketIO(app)
api = Api(app)

TABLE_TYPE = {1:"user",2:""}

def resource_type(table_name):

    resource_fields = {}

    if(table_name == "note" ):
        resource_fields = {
        'id': fields.Integer,
        'data': fields.String,
        'date': fields.Integer,
        'user_id': fields.Integer}
    
    if(table_name == "user"):
        resource_fields = {
        'id': fields.Integer,
        'email': fields.String,
        'password': fields.String,
        'first_name': fields.String}
    
    if(table_name == "channel"):
        resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'user_id': fields.String}
    
    if(table_name == "team"):
        resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'user_id': fields.String}


class HelloWorld(Resource):
    @marshal_with(resource_fields)
    def get(self,video_id):
        if(video_id):
            result = VideoModel.query.filter_by(id=video_id).first()
            
        if not result:
            abort(404, message="Could not find video with that id")
        return result, 200

    @marshal_with(resource_fields)
    def put(self,video_id):
        args = video_put_args.parse_args()

        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="video id taken...")

        video = VideoModel(id=video_id,name=args['name'], views = args['views'],likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self,video_id):
        args = video_update_args.parse_args()
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

class GetAll(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = VideoModel.query.all()
            
        if not result:
            abort(404, message="Could not find any videos")
        return result, 200

    @marshal_with(resource_fields)
    def post(self):     
        args = video_put_args.parse_args()
        
        result = VideoModel.query.all()

        if result:
            result = result[-1].id
            video = VideoModel(id=result+1,name= args['name'], views = args['views'],likes = args['likes'])
        if not result:
            print("Not result happened!")
            video = VideoModel(id=1, name= args['name'], views = args['views'], likes = args['likes'])
    
        db.session.add(video)
        db.session.commit()

        return video,201
        '''