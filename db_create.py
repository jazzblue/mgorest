#!flask/bin/python

#from migrate.versioning import api
#from config import SQLALCHEMY_DATABASE_URI
#from config import SQLALCHEMY_MIGRATE_REPO

#import os.path
from mgorest.v1_0.models import User
from mgorest import db, app

users = [
    dict(login='paul', password='paul1234', first_name='Paul', last_name='M.', occupation='Musician', city='London'),
    dict(login='ritchie', password='ritch1234', first_name='Ritchie', last_name='B.', occupation='Musician', city='London'),
    dict(login='bob', password='bob1234', first_name='Bob', last_name='N.', occupation='Actor', city='Los Angeles'),
    dict(login='steve', password='steve1234', first_name='Steve', last_name='V.', occupation='Musician', city='Los Angeles'),
    dict(login='amy', password='amy1234', first_name='Amy', last_name='B.', occupation='Musician', city='Los Angeles'),
    dict(login='jason', password='jason1234', first_name='Jason', last_name='L.', occupation='Actor', city='Los Angeles'),
    dict(login='David', password='david1234', first_name='David', last_name='G.', occupation='Musician', city='Los Angeles'),
    dict(login='stanley', password='stanley1234', first_name='Stanley', last_name='T.', occupation='Actor', city='London'),
    dict(login='peter', password='peter1234', first_name='Peter', last_name='T.', occupation='Actor', city='London'), 
    dict(login='kate', password='kate1234', first_name='Kate', last_name='L.', occupation='Actor', city='New York')
]

with app.app_context():

    db.create_all()

    for user in users:

        user_entry = User()

        for data_type in user:
            setattr(user_entry, data_type, user[data_type])

        db.session.add(user_entry)

    db.session.commit()

    print User.query.all()
