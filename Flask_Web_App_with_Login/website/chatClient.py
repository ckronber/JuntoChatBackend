import socketio
sio = socketio.AsyncClient()

@sio.event
def connect():
    print("I am connected")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm Disconnected!")

@sio.event
def message(data):
    print(data)
    return data


