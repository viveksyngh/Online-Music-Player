#### imports ####
#################

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
import os

################
#### config ####
################

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = '\xd9Wvyg\x86\x9e*\xc4}\x15\x85\xb5ms\r\xb0E\x11\xbe\r`\xe1\xbd'
#app.database = "sample.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://btxtrmxejekcle:W4M4DI3eXD22MtvDX7ILKDIYHE@ec2-54-204-15-48.compute-1.amazonaws.com:5432/d42s8frif1eaa5'

#create the db
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.home.views import home_blueprint

# register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)
