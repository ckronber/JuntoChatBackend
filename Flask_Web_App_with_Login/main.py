from website import create_app
from flask_socketio import SocketIO

HOST = "localhost"
PORT = 3000

PORTEXISTS=True

app = create_app()
socketio = SocketIO(app)

if __name__ == "__main__":
    if(PORTEXISTS):
        socketio.run(app,host=HOST,port = PORT,debug=True)
    else:
        socketio.run(app,host=HOST,debug=True)