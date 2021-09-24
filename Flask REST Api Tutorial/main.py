from flask import Flask,jsonify,request,render_template
from flask_restful import Api, Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy
import socketio
from sqlalchemy_utils.functions import database_exists
from flask_socketio import SocketIO,send,emit

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'BestEverPassword'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///VideoDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socket = SocketIO(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    views = db.Column(db.Integer,nullable=False)
    likes = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"Video(name={self.name}, views = {self.views}, likes = {self.likes}"

resource_fields = {'id': fields.Integer,
                   'name': fields.String,
                   'views': fields.Integer,
                   'likes': fields.Integer}

if(database_exists(app.config['SQLALCHEMY_DATABASE_URI'])):
    pass
else:
    db.create_all() # only used the first time to setup the database

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required",required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required",required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video is required",required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video is required")
video_update_args.add_argument("likes", type=int, help="Likes of the video is required")

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

api.add_resource(GetAll,"/video")
api.add_resource(HelloWorld,"/video/<int:video_id>")

if __name__ == "__main__":
    app.run(host='localhost',port = 3000,debug=True)