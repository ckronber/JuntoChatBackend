import  requests
from datetime import datetime,timezone, tzinfo
from time import sleep
from main import HelloWorld,GetAll
from models import VideoModel
from flask_sqlalchemy import SQLAlchemy
from flask_restful import fields

#Base = "http://127.0.0.1:3000/"

#data = [ {"likes":78,"name":"Chris","views":1000000},  
#         {"likes":56748,"name":"How to make REST API","views":10000000},  
#         {"likes":4567,"name":"my 3rd video","views":5482158}]
#for i in range(len(data)):
#    response = requests.put(Base+"video/"+str(i),data[i])
#    print(response.json()) 

#response = requests.patch(Base+"video/2", {"views":99,"likes":101})
#print(response.json())

"""def get_time(time_format:int):
    time_stamp = {"year":datetime.now().year,"month":datetime.now().month,"day":datetime.now().day,"hour":datetime.now().hour,"minute":datetime.now().minute,"second":datetime.now().second}

    if(time_format == 1):
        return f"{time_stamp['month']}/{time_stamp['day']}/{time_stamp['year']}  {time_stamp['hour']}:{time_stamp['minute']}:{time_stamp['second']}"
    if(time_format == 2):
        return f"{time_stamp['hour']}:{time_stamp['minute']}:{time_stamp['second']}"
    
    if(time_format == 3):
        return f"{time_stamp['month']}/{time_stamp['day']}/{time_stamp['year']}"

print(get_time(1))
"""