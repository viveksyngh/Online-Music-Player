from project import app, db
from project.model import User

# insert data
db.session.add(User("michael", "michael@realpython.com", "i'll-never-tell"))
db.session.add(User("admin", "ad@min.com", "admin"))
db.session.add(User("mike", "mike@herman.com", "tell"))

# commit the changes
db.session.commit()