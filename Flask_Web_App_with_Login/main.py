from website import create_app
from website.views import sio

HOST = "127.0.0.1"
PORT = 3000

app = create_app()
sio.init_app(app)
#client = socketio.test_client(app)

if __name__ == "__main__":
    sio.run(app,host=HOST,port = PORT,debug=True)