
from mgorest import db

#from mgo.app_init import app

#print 'models:', app.config['SQLALCHEMY_DATABASE_URI']


#class Sighting(db.Model):
#  __tablename__ = 'sightings'
#  id = db.Column(db.Integer, primary_key = True)
#  sighted_at = db.Column(db.Integer)
#  reported_at = db.Column(db.Integer)
#  location = db.Column(db.String(100))
#  shape = db.Column(db.String(10))
#  duration = db.Column(db.String(10))
#  description = db.Column(db.Text)
#  lat = db.Column(db.Float(6))
#  lng = db.Column(db.Float(6))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=False, unique=False)
    first_name = db.Column(db.String(64), index=False, unique=False)
    last_name = db.Column(db.String(64), index=False, unique=False)
    occupation = db.Column(db.String(64), index=False, unique=False)
    city = db.Column(db.String(64), index=False, unique=False)

    def __repr__(self):
        return '<User %r>' % (self.login)
