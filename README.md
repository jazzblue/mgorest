# MGOREST

## Description
A simple Webservice using flask-SQLAlchemy Python framework. The project contains versioning support and unittesting.

## Deployment
1. Install python2.7
2. Set PYTHONPATH environment variable to point to root of the project, for example if you use bash: *export PYTHONPATH=/home/mylogin/projects/mgorest*

3. I used MySQL as RDBMS for this project. If you intend to use MySQl as well make sure you have all the needed drivers, for example on Ubuntu you migh need: *sudo apt-get install libmysqlclient-dev*

4. Install following Python libraries (if you install using pip, make sure you have pip installed and then install: *pip install <library>*):

* flask
* flask-sqlalchemy
* mysql-python

## Versioning support
I am using flask Blueprints to easily support different versions.

## Unittesting
Unitest is per version. Currently there is only one version **v1_0**. You can find it in the file *mgorest/v1_0/tests.py*. You can run it:

*cd into mgorest/v1_0/ directory.*
*python tests.py*

## Webservice sample usage
Here is the example on how you can try out the webservice API using Python.

1. Start the Server.
* - cd into inner mgorest/

2. Install Python library requests, e.g. *pip install requests*.

3. Run python shell.
*
import requests
payload = {'login': 'bob', 'password': 'bob1234'}
r = requests.post("http://localhost:5000/auth", json=payload)
r.json()
*
