from mgorest import db

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
