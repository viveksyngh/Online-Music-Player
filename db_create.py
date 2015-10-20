from project import app, db
from project.model import BlogPost, User, Track

#create the database and the db tablse

#db.create_all()

#insert

#db.session.add(BlogPost("Good", "I\' m good."))
#db.session.add(BlogPost("Well", "I\' m Well. "))

db.session.add(Track("Songs.PK_01_-_Jackpot_-_Kabhi_Jo_Baadal_Barse.mp3", "project\home\uploads\Songs.PK_01_-_Jackpot_-_Kabhi_Jo_Baadal_Barse.mp3", 2, 1, 1))
#db.session.add(Track("Well", "I\' m Well. "))


#commit

db.session.commit()
