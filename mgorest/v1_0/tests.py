import unittest
from mgorest import db, app
from mgorest.v1_0.models import User
import json

import logging

logging.basicConfig(level=logging.DEBUG)
mgo_logger = logging.getLogger(__name__)
mgo_logger.setLevel(logging.INFO)

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('mgorest.configmodule.TestingConfig')  # Import test configuration
        
        mgo_logger.debug('test DB: ' + app.config['SQLALCHEMY_DATABASE_URI'])

        self.test_app = app.test_client()

        # Populate test DB.
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

        app.config.from_object('mgorest.configmodule.TestingConfig')  # Import test configuration

        with app.test_request_context():
            db.session.remove()
            db.drop_all()

    def test_auth_success(self):
        """Tests successful authentication."""

        login = 'bob'
        password = 'bob1234'  # correct password

        # Call webservice.
        rv = self.test_app.post('/auth', data=json.dumps(dict(login=login, password=password)), content_type = 'application/json')

        response = json.loads(rv.data)

        assert 'login' in response
        assert response['login'] == login
        assert 'authentication_status' in response
        assert response['authentication_status'] == 'Success'

    def test_auth_fail(self):
        pass
        """Tests failed authentication."""

        login = 'bob'
        password = 'bob5678'  # wrong password

        # Call webservice.
        rv = self.test_app.post('/auth', data=json.dumps(dict(login=login, password=password)), content_type = 'application/json')

        response = json.loads(rv.data)

        assert 'login' in response
        assert response['login'] == login
        assert 'authentication_status' in response
        assert response['authentication_status'] == 'Fail'

    def test_filter_no_paginate(self):
        """Tests "filter" webservice with no pagination. Expects user logins by occupation, from London. """
        rv = self.test_app.get('/filter?city=London')
        assert json.loads(rv.data) == {u'Musician': [u'paul', u'ritchie'], u'Actor': [u'stanley', u'peter']}

    def test_filter_paginate_1(self):
        """Tests "filter" webservice with pagination. Expects user logins by occupation, from London. """
        rv = self.test_app.get('/filter/1?city=London')
        assert json.loads(rv.data) == {u'Musician': [u'paul'], u'Actor': [u'stanley', u'peter']}

    def test_filter_paginate_2(self):
        """Tests "filter" webservice with pagination. Expects user logins by occupation, from London. """
        rv = self.test_app.get('/filter/2?city=London')
        assert json.loads(rv.data) == {u'Musician': [u'ritchie']}

    def test_systemcheck_ok(self):
        """Tests systemcheck webservice. Verifies that DB and disc have OK status in regular situation."""

        rv = self.test_app.get("/systemcheck")
        assert json.loads(rv.data) == dict(db_status='OK', disc_status='OK')

    def test_systemcheck_db_fail(self):
        """Tests systemcheck webservice. Simulates DB failure and verifies that DB status is fail."""

        # Corrupt db name, i.e. simulate DB failure.
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sqlrootpw@localhost/xxx'
        rv = self.test_app.get("/systemcheck")
        assert json.loads(rv.data) == dict(db_status='Fail', disc_status='OK')

    def test_listdir_success(self):
        """Tests listdir webservice. Verifies that contents of existing directory are listed successfully."""
        # TBD: this tests depends on deployment, i.e. what directories/files are on deployment machine.
        # I will leave it empty for the purpose of thos project.
        pass


    def test_listdir_fail(self):
        """TBD: Tests listdir webservice. Verifies that listing non-exiting directory returns appropriate response."""
        pass

    

if __name__ == '__main__':
    unittest.main()
