from flask import Blueprint,render_template,request,jsonify,redirect
from flask.helpers import url_for

views = Blueprint(__name__,"/")

@views.route('/')
def home():
    return render_template("index.html", name = "Chris")


#returning an html file
@views.route('/profile1')
def profile1():
    args = request.args
    name = args.get('name')
    return render_template("index.html", name = name)

#returning json
@views.route("/json")
def get_json():
    return jsonify({"Name":"Chris","Awesomeness":["A","B"]})


@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

#redirect
@views.route("/go-to-home")
def goHome():
    return redirect(url_for("views.get_json"))


@views.route('/profile')
def profile():
    return render_template("profile.html")
