#### imports ####
#################
from project import app, db
from project import ALLOWED_EXTENSIONS
from project.model import BlogPost, User
from flask import flash, redirect, session, url_for, render_template, Blueprint, request
from functools import wraps
from forms import MessageForm
from flask.ext.login import login_user, current_user, login_required
from werkzeug import secure_filename
import os

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)

'''

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
.'''
@home_blueprint.route('/', methods=['GET', 'POST'])   # pragma: no cover
@login_required   # pragma: no cover
def home():
    error = None
    form = MessageForm(request.form)
    if form.validate_on_submit():
        new_message = BlogPost(
            form.title.data,
            form.description.data,
            current_user.id
        )
        db.session.add(new_message)
        db.session.commit()
        flash('New entry was successfully posted. Thanks.')
        return redirect(url_for('home.home'))
    else:
        posts = db.session.query(BlogPost).all()
        songs = os.listdir(os.path.abspath(app.config['UPLOAD_FOLDER']))
        return render_template(
            'index.html', posts=posts, form=form, error=error, songs=songs, folder=os.path.abspath(app.config['UPLOAD_FOLDER']))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#@home_blueprint.route('/uploader')
#def uploader() :
#   return render_template("upload.html")


@home_blueprint.route('/upload', methods=['GET', 'POST'])   # pragma: no cover
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home.home'))
    return render_template("upload.html")

#@home_blueprint.route('/')
#@login_required
#def home() :
#	#return "Hello, World!"
#	posts = db.session.query(BlogPost).all()
#	return render_template('index.html', posts=posts)

@home_blueprint.route('/welcome')
def welcome() :
	return render_template("welcome.html")
