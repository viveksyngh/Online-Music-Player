from flask import Flask, render_template, url_for, request, redirect, session, flash, g
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
#import sqlite3


app = Flask(__name__)
app.secret_key = "My Previous"
#app.database = "sample.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

#create the db
db = SQLAlchemy(app)

from model import *


#Login required Decorators
def login_required(f) :
	@wraps(f)
	def wrap(*args, **kwargs) :
		if 'logged_in' in session :
			return f(*args, **kwargs)
		else :
			flash("You need to login first.")
			return redirect(url_for('login'))
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
	return redirect(url_for('welcome'))

#def connect_db():
#	return sqlite3.connect(app.database)

if __name__ == '__main__' :
	app.run(debug=True)
