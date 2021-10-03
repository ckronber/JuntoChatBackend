from aiohttp import web
import socketio
import socket
import threading
import os

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    print (f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while(connected):
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                
            print(f"[{addr}] {msg}")
            conn.send("Msg Received".encode(FORMAT))

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        con, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(con,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


print("[STARTING] Server is starting")
start()

""""
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    "Serve the client-side application."
    with open('./ExampleChatApp/index.js') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.event
def connect(sid, environ):
    print("connect", sid)

@sio.event
async def chat_message(sid, data):
    print("message ", data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

#app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app,port=3000)
"""