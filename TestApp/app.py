from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,RadioField,PasswordField
from views import views

app = Flask(__name__)
app.config['Secret_Key'] = "BestSecret"

app.register_blueprint(views,url_prefix="/")

if __name__ == '__main__':
    app.run(debug=True,port=5000)