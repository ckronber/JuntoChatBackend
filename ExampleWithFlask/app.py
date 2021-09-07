from flask import Flask
from helper import pets

app = Flask(__name__)

@app.route("/")
def index():
  return f"""
  <h1>Adopt A Pet!</h1>
  <p>Browse through the links below to find your new furry friend:</p>

  <ul>
    <a href="/animals/dogs"><li>Dogs</li></a>
    <a href="/animals/cats"><li>Cats</li></a>
    <a href="/animals/rabbits"><li>Rabbits</li></a>
  </ul>
  """

@app.route("/animals/<pet_type>")
def animals(pet_type):
  listPets = ""
  for mypet in pets[pet_type]:
    listPets += f"<li>{mypet}</li>"
  return f"""
    <h1>List of {pet_type.title()}</h1>
    <ul>{listPets}</ul>
    <a href="/">Back to Home</a>
  """

@app.route("/animals/<string:pet_type>/<int:pet_id>",methods=["GET"])
def pet(pet_type,pet_id):
  pet = {}
  for idx,mypet in enumerate(pets[pet_type]):
    if(idx+1 == pet_id):
      pet = mypet
  return f"""
  <!DOCTYPEHTML>
    <html>
      <head>
        <link rel="stylesheet" href="main.css">
      </head>
      <body>
        <h1 class="firstClass">{(pet_type.title()).replace("s","")} #{pet_id}</h1>
        <img src="{pet['url']}" alt="Dog Image{pet_id}"/>
        <p>{pet['description']}</p>
        <ul>
          <li>
            Breed:{pet['breed']}
          </li>
          <li>
            Age:{pet['age']}
          </li>
        </ul>
        <a href="/">Back to Home</a>
      </body>
    </html>
  """
