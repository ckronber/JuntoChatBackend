from website import create_app

HOST = "localhost"
PORT = 3000

portExists =True

app = create_app()

if __name__ == "__main__":
    if(portExists):
        app.run(host=HOST,port = PORT,debug=True)
    else:
        app.run(host=HOST,debug=True)