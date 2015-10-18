#################
#### imports ####
#################

from flask import flash, redirect, render_template, request, \
    session, url_for, Blueprint
from functools import wraps
#from forms import LoginForm
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


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap


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
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home.home'))

        #if (request.form['username'] != 'admin') \
        #        or request.form['password'] != 'admin':    
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@users_blueprint.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('home.welcome'))