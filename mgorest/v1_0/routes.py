from flask import Blueprint, request, jsonify, abort
from mgorest import db
from models import User
from mgorest.configmodule import ENTRIES_PER_PAGE
from flask import make_response
import os
import json

import logging

logging.basicConfig(level=logging.INFO)
mgo_api_logger = logging.getLogger(__name__)

api = Blueprint('api_v1_0', __name__)

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found.'}), 404)

@api.route('/auth', methods=['POST'])
def auth():
    """
    Authenticates user with based on a login/password passed in a JSON payload.
    return: JSON format of the following structure:
             {"login": <requested login>, "authentication_status": "Success"/"Fail", based on authentication result.}
              
    """
    mgo_api_logger.debug('data: ' + str(request.get_data()))
    mgo_api_logger.debug('json: ' + str(request.get_json()))

    if not request.get_json() or 'login' not in request.get_json():
        abort(400)

    user = User.query.filter_by(login=request.json['login']).first()

    if user is None:  # User is not in DB.
        abort(404)
    elif user.password == request.get_json()['password']:  # Password match.
        return jsonify({'login': user.login, 'authentication_status': 'Success'})
    else:  # Password does not match.
        return jsonify({'login': user.login, 'authentication_status': 'Fail'})

@api.route('/filter', methods=['GET'])
@api.route('/filter/<int:page>', methods=['GET'])
def filter_and_group(page=None):
    """
    Filters by city, groups by occupation.
    return: JSON of the shape:
        {<occupation1>: [<login1>, <login2>, ...], <occupation1>: [<login1>, <login2>, ...], ...}
    """
    city = request.args.get('city')

    if page is None:  # page is not specified in URL, do not paginate.
        query_result = User.query.with_entities(User.login, User.occupation).filter_by(city=city).order_by(User.occupation).all()

    else: # page is specified in URL, paginate.
        query_result = User.query.with_entities(User.login, User.occupation).filter_by(city=city).order_by(User.occupation).paginate(page, ENTRIES_PER_PAGE, False).items

    mgo_api_logger.debug('filter-n-group: ' + str(query_result))

    # Create table of occupations containing list of users per occupation
    occupation_users = dict()

    for u in query_result:   # In query_result, for each tuple, user is at index 0, occupation is at index 1
        if u[1] not in occupation_users:  # If occupation is not in the table, create a new occupation with empty list
            occupation_users[u[1]] = list()
        occupation_users[u[1]].append(u[0])  # Append user login to corresponding occupation list

    mgo_api_logger.debug('occupation_users: ' + str(occupation_users))

    return jsonify(occupation_users)

@api.route('/systemcheck', methods=['GET'])
def system_check():
    """
    return: list of all components this webservice depends on: DB, disc: {'db_status': 'OK'/'Fail', 'disc_status': 'OK'/'Fail'}
    """

    # MySQL check: run a simple short query that should not fail if DB is up.
    try:
        user = User.query.first()
        db_status = 'OK'
    except:
        db_status = 'Fail'
    
    # Disc check: we will try to get contents of root directory "/" it should always work if the disc is up.
    try:
        dir_list = os.listdir('/')
        disc_status = 'OK'
    except:
        disc_status = 'Fail'

    return json.dumps(dict(db_status=db_status, disc_status=disc_status))

@api.route('/listdir', methods=['GET'])
def list_dir():
    """
    return: list of files in a directory specified by "dir" argument.
    """
    dir =  request.args.get('dir')

    try:
        dir_list = os.listdir(dir)
    except Exception as e:  # directory not found.

        mgo_api_logger.debug('listdir error: ' + str(e))

        abort(404)
    else:        
        mgo_api_logger.debug('listdir: ' + str(dir_list))

        return json.dumps(dir_list)

    
