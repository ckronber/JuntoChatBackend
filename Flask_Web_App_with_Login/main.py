from website import create_app
from website.views import socketio

HOST = "127.0.0.1"
PORT = 3000

app = create_app()
socketio.init_app(app)
#client = socketio.test_client(app)

if __name__ == "__main__":
    socketio.run(app,host=HOST,port = PORT,debug=True)
