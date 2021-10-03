from flask_socketio import SocketIO
from website import create_app
from flask_socketio import SocketIO
from website.chatserver import socketio

HOST = "localhost"
PORT = 3000

PORTEXISTS=True

app = create_app()
socketio.init_app(app)

if __name__ == "__main__":
    if(PORTEXISTS):
        socketio.run(app,host=HOST,port = PORT,debug=True)
    else:
        socketio.run(app,host=HOST,debug=True)