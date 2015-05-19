# MGOREST

## Description
A simple Webservice using flask-SQLAlchemy Python framework. The project contains versioning support and unittesting.

## Framework choice
I chose to use Flask-SQLAlchemy for this project due to the fact that it is relatively lightweight (especally Flask) and it is quite easy to set up and start coding away, adding on incrementally. 

## Deployment
1. Install python2.7
2. Set PYTHONPATH environment variable to point to root of the project, for example if you use bash: *export PYTHONPATH=/home/mylogin/projects/mgorest*

3. I used MySQL as RDBMS for this project. If you intend to use MySQL as well make sure you have all the needed drivers, for example on Ubuntu you migh need: *sudo apt-get install libmysqlclient-dev*

4. Install following Python libraries (if you install using pip, make sure you have pip installed and then install: *pip install <library>*):

* flask
* flask-sqlalchemy
* mysql-python

## Versioning support
I am using flask Blueprints to easily support different versions.

## Unittesting
Unitest is per version. Currently there is only one version **v1_0**. You can find it in the file *mgorest/v1_0/tests.py*. You can run it:

*cd into mgorest/v1_0/ directory.*

*>python tests.py*

## Pagination
TBD

## Webservice sample usage

Here is the example on how you can try out the webservice API using Python.

### Populate DB
You can populate DB using the following script in the outer **mgorest** directory. Note that if you want to use this script multiple times, you will need to drop the **users** table, each time prior to usage, otherwise, you will get "Primary key conflicts":

*>python db_create.py*

### Run 
1. Start the Server.

*cd into inner mgorest/*

2. Install Python library requests, e.g. 

*>pip install requests*.

3. Run python shell. Then:

*>>>import requests*

*>>>payload = {'login': 'bob', 'password': 'bob1234'}*

*>>>r = requests.post("http://localhost:5000/auth", json=payload)*

*>>>r.json()*
