
class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'mysql://root:sqlrootpw@localhost/mgo'  # DB type: mysql, login: root, password: sqlrootpw, DB URL: localhost, DB: mgo  

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:sqlrootpw@localhost/mgo'  # DB type: mysql, login: root, password: sqlrootpw, DB URL: localhost, DB: mgo 


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:sqlrootpw@localhost/mgo_test' # DB type: mysql, login: root, password: sqlrootpw, DB URL: localhost, DB: mgo 
