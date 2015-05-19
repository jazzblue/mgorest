# MGOREST

## Description
A small Webservice using flask-SQLAlchemy Python framework. The project contains versioning support, pagination support and unittesting. The webservice consists of four endpoints:

- Endpoint that authenticates a user based on a login/password passed in a JSON payload and verifies against MySQL.

    *POST http://localhost:5000/auth*

    *JSON payload : {'login': 'bob', 'password': 'bob1234'}*

**Note: the latest version (v1_0) is default, however, you can also explicitly specify version in URL, e.g.**

*POST http://localhost:5000/v1_0/auth*

*JSON payload : {'login': 'bob', 'password': 'bob1234'}*

- Endpoint that returns all users in the database filtered by city (as a URL parameter) and groups them by occupation.

without pagination:

 *GET http://localhost:5000/filter?city=London*

with pagination:

 *GET http://localhost:5000/filter/1?city=London*

- Endpoint that checks and returns the status of all components that it depends on: DB, disc.

*GET http://localhost:5000/systemcheck*

- Endpoint that when called returns the list of files in a given directory.

*GET http://localhost:5000/listdir?dir=/home/mylogin/projects* 

## Stack
As a framework I chose to use Flask-SQLAlchemy for this project due to the fact that it is relatively lightweight, quite easy to set up and start coding away, adding on incrementally. For DB I am using MySQL as it is an adequate choice for the given requirements: the data can easily utilize relational model.

## Deployment
1. Install python2.7
2. Set PYTHONPATH environment variable to point to the root of the project, for example if you use bash: *export PYTHONPATH=/home/mylogin/projects/mgorest*

3. I used MySQL as RDBMS for this project. If you intend to use MySQL as well make sure you have all the needed drivers, for example on Ubuntu you migh need: *sudo apt-get install libmysqlclient-dev*

4. Install following Python libraries (if you install using pip, make sure you have pip installed and then install: *pip install <library>*):

  * flask
  * flask-sqlalchemy
  * mysql-python

5. In the file **mgorest/configmodule.py** configure you database for development and testing by setting SQLALCHEMY_DATABASE_URI variable.


## Versioning support
I am using flask Blueprints to easily support different versions. Each version should be put in a directory under inner **mgorest/** folder. Simply register new blueprint for new version in *mgorest/\_\_init\_\_.py* (inner *mgorest*).

Currently there is only one version **v1_0** and it is also registered as default version, i.e. it can be either specified or omitted in URL.

## Unittesting
Unitest is per version. Currently there is only one version **v1_0** and the tests could be found in the file *mgorest/v1_0/tests.py*.
The file contains a number of important tests, however, I do not claim full coverage here which is not the purpose of this project. The purpose is to have an adequate infrustructure allowing for easy addition of new tests if needed.


The tests can be run by:

*cd into mgorest/v1_0/ directory.*

*>python tests.py*

## Pagination
Pagination is supported for the "filter" webservice. It is easily implemented using Flask-SQLAlchemy **paginate** method. If the page is specified in the URL then the response is paginated, otherwise, if page is omitted from URL, the response is not paginated.

## Webservice sample usage

Here is the example on how you can try out the webservice API using Python:

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
