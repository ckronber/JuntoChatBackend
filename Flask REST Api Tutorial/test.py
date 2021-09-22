import  requests

Base = "http://127.0.0.1:3000/"

data = [ {"likes":78,"name":"Chris","views":1000000},  
         {"likes":56748,"name":"How to make REST API","views":10000000},  
         {"likes":4567,"name":"my 3rd video","views":5482158}]
for i in range(len(data)):
    response = requests.put(Base+"video/"+str(i),data[i])
    print(response.json()) 

response = requests.patch(Base+"video/2", {"views":99,"likes":101})
print(response.json())