from project import app, db
from project.model import BlogPost, User, Track

#create the database and the db tablse

db.create_all()

#insert

#db.session.add(BlogPost("Good", "I\' m good."))
#db.session.add(BlogPost("Well", "I\' m Well. "))


#commit

db.session.commit()
