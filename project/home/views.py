#### imports ####
#################
from project import app, db
from project import ALLOWED_EXTENSIONS
from project.model import BlogPost, User, Track, Track_Vote
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
        tracks = db.session.query(Track).order_by(Track.upvote.desc()).all()
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
                os.path.join(app.config['UPLOAD_FOLDER'].replace('project','..'), filename), 
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
        select_votes = Track_Vote.query.filter_by(user_id=current_user.id, track_id=track_id).first()
        if select_votes == None :
            new_vote = Track_Vote(track_id,
                current_user.id,
                1,
                0)
            db.session.add(new_vote)
            #db.session.commit()
            track.upvote += 1
            #db.session.commit()
        elif select_votes.upvote_flag == 0 :
            select_votes.upvote_flag = 1
            track.upvote += 1
            if select_votes.downvote_flag == 1:
            #db.session.commit()
                track.downvote -= 1
                select_votes.downvote_flag = 0
            #db.session.commit()
        else :
            select_votes.upvote_flag = 0
            #db.session.commit()
            track.upvote -= 1
            #db.session.commit()
        #track_id = request.form['id']
        #track = Track.query.filter_by(id=request.form['id']).first()
        db.session.commit()
    return redirect(url_for('home.home'))

@home_blueprint.route('/downvote', methods=['GET', 'POST']) 
def downvote() :
    if request.method == 'POST' :
        track_id = request.form['id']
        track = Track.query.filter_by(id=request.form['id']).first()
        select_votes = Track_Vote.query.filter_by(user_id=current_user.id, track_id=track_id).first()
        if select_votes == None:
            new_vote = Track_Vote(track_id,
                current_user.id,
                0,
                1)
            db.session.add(new_vote)
            #db.session.commit()
            track.downvote += 1
            #db.session.commit()
        elif select_votes.downvote_flag == 0 :
            select_votes.downvote_flag = 1
            track.downvote += 1
            if select_votes.upvote_flag == 1 :
                select_votes.upvote_flag = 0
            #db.session.commit()
                track.upvote -= 1
            #db.session.commit()
        else :
            select_votes.downvote_flag = 0
            #db.session.commit()
            track.downvote -= 1
            #db.session.commit()
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
