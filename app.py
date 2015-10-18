#### imports ####
#################

from flask import Flask, flash, redirect, session, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
import os

################
#### config ####
################

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
app.register_blueprint(users_blueprint)

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

@app.route('/')
@login_required
def home() :
	#return "Hello, World!"
	posts = db.session.query(BlogPost).all()
	return render_template('index.html', posts=posts)

@app.route('/welcome')
def welcome() :
	return render_template("welcome.html")

'''
@app.route('/login', methods=['GET', 'POST'])
def login() :
	error = None
	if request.method == 'POST' :
		if request.form['username'] != 'admin' or request.form['password'] != 'admin' :
			error = 'Invalid Credentaials. Please try again.'
		else :
			session['logged_in'] = True
			flash("You have just logged in")
			return redirect(url_for('home'))
	return render_template('login.html', error=error) 

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash("You have logged out")
	return redirect(url_for('welcome')) '''

#def connect_db():
#	return sqlite3.connect(app.database)

####################
#### run server ####
####################

if __name__ == '__main__' :
	app.run(debug=True)
