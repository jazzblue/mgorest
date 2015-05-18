from flask import Blueprint, request, jsonify, abort
from mgorest import db
from models import User
from flask import make_response

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

