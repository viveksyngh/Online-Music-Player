#### imports ####
#################
from project import app, db
from project import ALLOWED_EXTENSIONS
from project.model import BlogPost, User, Track
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
        tracks = db.session.query(Track).all()
        user = User.query.filter_by(id=current_user.id).first()
        #songs = os.listdir(os.path.abspath(app.config['UPLOAD_FOLDER']))
        #folder=os.path.abspath(app.config['UPLOAD_FOLDER'])
        return render_template(
            'index.html', form=form, error=error, tracks=tracks, username=user.name)


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
            new_track = Track(
                filename, 
                os.path.join(app.config['UPLOAD_FOLDER'], filename), 
                current_user.id,
                0, 0
                )
            db.session.add(new_track)
            db.session.commit()
            flash('New song was successfully uploaded. Thanks.')
            return redirect(url_for('home.home'))
    return render_template("upload.html")


@home_blueprint.route('/upvote', methods=['GET', 'POST']) 
def upvote() :
    if request.method == 'POST' :
        track_id = request.form['id']
        track = Track.query.filter_by(id=request.form['id']).first()
        track.upvote += 1
        db.session.commit()
    return redirect(url_for('home.home'))

@home_blueprint.route('/downvote', methods=['GET', 'POST']) 
def downvote() :
    if request.method == 'POST' :
        track_id = request.form['id']
        track = Track.query.filter_by(id=request.form['id']).first()
        track.downvote += 1
        db.session.commit()
    return redirect(url_for('home.home'))



#@home_blueprint.route('/')
#@login_required
#def home() :
#	#return "Hello, World!"
#	posts = db.session.query(BlogPost).all()
#	return render_template('index.html', posts=posts)

@home_blueprint.route('/welcome')
def welcome() :
	return render_template("welcome.html")