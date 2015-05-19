import unittest
#import os

#from config import basedir
#from mgo.models_common import APP_MODE
#APP_MODE = 'Testing'

#from models import db, User
from mgorest import db, app
from mgorest.v1_0.models import User
#from mgorest import configmodule
#from app.models import User
#import requests
#from flask import jsonify
import json

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('mgorest.configmodule.TestingConfig')  # Import configuration

#        app.config['TESTING'] = True
#        app.config['WTF_CSRF_ENABLED'] = False
#        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sqlrootpw@localhost/mgo_test'

        self.test_app = app.test_client()

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

        with app.test_request_context():

            db.create_all()

            for user in users:

                user_entry = User()

                for data_type in user:
                    setattr(user_entry, data_type, user[data_type])

                db.session.add(user_entry)

            db.session.commit()


    def tearDown(self):
        with app.test_request_context():
            db.session.remove()
            db.drop_all()

    def test_auth_success(self):
        login = 'bob'
        password = 'bob1234'

        rv = self.test_app.post('/auth', data=json.dumps(dict(login=login, password=password)), content_type = 'application/json')

        response = json.loads(rv.data)

        assert 'login' in response
        assert response['login'] == login
        assert 'authentication_status' in response
        assert response['authentication_status'] == 'Success'

    def test_auth_fail(self):
        pass

    def test_filter(self):
        rv = self.test_app.get('/filter?city=London')
        assert json.loads(rv.data) == {u'Musician': [u'paul', u'ritchie'], u'Actor': [u'stanley', u'peter']}

    def test_resources(self):
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sqlrootpw@localhost/mgo_tes'
        pass

if __name__ == '__main__':
    unittest.main()
