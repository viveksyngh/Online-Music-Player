#### imports ####
#################
from project import app, db
from project.model import BlogPost
from flask import flash, redirect, session, url_for, render_template, Blueprint
from functools import wraps

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)

'''
app = Flask(__name__)
#bcrypt = Bcrypt(app)
app.secret_key = '\xd9Wvyg\x86\x9e*\xc4}\x15\x85\xb5ms\r\xb0E\x11\xbe\r`\xe1\xbd'
#app.database = "sample.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://btxtrmxejekcle:W4M4DI3eXD22MtvDX7ILKDIYHE@ec2-54-204-15-48.compute-1.amazonaws.com:5432/d42s8frif1eaa5'

#create the db
db = SQLAlchemy(app)

from model import *
from project.users.views import users_blueprint

# register our blueprints
app.register_blueprint(users_blueprint) '''

#Login required Decorators
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap

@home_blueprint.route('/')
@login_required
def home() :
	#return "Hello, World!"
	posts = db.session.query(BlogPost).all()
	return render_template('index.html', posts=posts)

@home_blueprint.route('/welcome')
def welcome() :
	return render_template("welcome.html")
