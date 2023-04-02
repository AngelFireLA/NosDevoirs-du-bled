from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login"  #
from routes import homework_routes
if __name__ == "__main__":
    app.run()
