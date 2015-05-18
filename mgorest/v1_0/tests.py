#import os
import unittest

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
            dict(login='bob', password='bob1234', first_name='Bob', last_name='N.', occupation='Actor', city='Los Angeles'),
            dict(login='amy', password='amy1234', first_name='Amy', last_name='B.', occupation='Musician', city='Los Angeles'),
            dict(login='jason', password='jason1234', first_name='Json', last_name='L.', occupation='Engineer', city='Los Angeles'),
            dict(login='stanley', password='stanley1234', first_name='Stanley', last_name='T.', occupation='Trader', city='London'),
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

    def test_auth(self):
        login = 'bob'
        password = 'bob1234'

        rv = self.test_app.post('/auth', data=json.dumps(dict(login=login, password=password)), content_type = 'application/json')

        response_json = json.loads(rv.data)

        assert 'login' in response_json
        assert response_json['login'] == login
        assert 'authentication_status' in response_json
        assert response_json['authentication_status'] == 'Success'

#        print r.json
#
#        assert True # r.json == jsonify({'login': login, 'password': password}) 
#
#    def test_make_unique_nickname(self):
#        u = User(nickname='john', email='john@example.com')
#        db.session.add(u)
#        db.session.commit()
#        nickname = User.make_unique_nickname('john')
#        assert nickname != 'john'
#        u = User(nickname=nickname, email='susan@example.com')
#        db.session.add(u)
#        db.session.commit()
#        nickname2 = User.make_unique_nickname('john')
#        assert nickname2 != 'john'
#        assert nickname2 != nickname

if __name__ == '__main__':
    unittest.main()
