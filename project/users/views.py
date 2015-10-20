#################
#### imports ####
#################

from flask import flash, redirect, render_template, request, \
    session, url_for, Blueprint
from flask.ext.login import login_user, login_required, logout_user
from functools import wraps
from forms import LoginForm, RegisterForm
from project import db, bcrypt
from project.model import User, bcrypt

################
#### config ####
################

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)

##########################
#### helper functions ####
##########################


################
#### routes ####
################

# route for handling the login page logic
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    #flash(user)
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['username']).first()
        #flash(user.name)
        #flash(user.password)
        #flash(result)
        if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
            #session['logged_in'] = True
            login_user(user)
            flash('You were logged in.')
            return redirect(url_for('home.home'))

        #if (request.form['username'] != 'admin') \
        #        or request.form['password'] != 'admin':    
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home.home'))
    return render_template('register.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
    #session.pop('logged_in', None)
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('home.welcome'))