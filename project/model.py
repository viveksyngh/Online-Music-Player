from project import db
from project import bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class BlogPost(db.Model):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, title, description, author_id):
        self.title = title
        self.description = description
        self.author_id = author_id

    def __repr__(self):
        return '<title {}'.format(self.title)



class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    posts = relationship("BlogPost", backref="author")
    track = relationship("Track", backref="uploaded_by")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<name - {}>'.format(self.name)
		

class Track(db.Model):

    """Model for storing track information"""

    __tablename__ = "track"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    uri = db.Column(db.String(200), unique=True)
    upvote = db.Column(db.Integer, nullable=False)
    downvote = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #track_id = db.Column(db.String(140), unique=True)


    def __init__(self, title, uri, user_id, upvote, downvote):
        self.title = title
        #self.track_id = track_id
        self.uri = uri
        self.user_id = user_id
        self.upvote = upvote
        self.downvote = downvote

    def __repr__(self):
        return '<Track %r>' % (self.title)

class Track_Vote(db.Model):
    
    """Model for tracking upvotes and downvotes by users""" 

    __tablename__ = "trackvote"

    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    upvote_flag = db.Column(db.Integer, nullable=False)
    downvote_flag = db.Column(db.Integer, nullable=False)


    def __init__(self, track_id, user_id, upvote_flag, downvote_flag):
        self.track_id = track_id
        self.user_id = user_id
        self.upvote_flag = upvote_flag
        self.downvote_flag = downvote_flag
    
        
        