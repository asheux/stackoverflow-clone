import logging
from flask import request
from flask_bcrypt import Bcrypt
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_raw_jwt,
    create_access_token
)
from stackoverflow.api.v1.auth.parsers import pagination_arguments
from stackoverflow import v2_api
from stackoverflow.api.v2.auth.serializers import (
    user_register,
    user_login,
    questions
)
from ..errors import check_valid_email, user_is_valid
from stackoverflow.api.v2.models import User, BlackList
from stackoverflow import settings

flask_bcrypt = Bcrypt()
log = logging.getLogger(__name__)
ns_auth = v2_api.namespace('auth', description='Authentication operations')
ns = v2_api.namespace('user', description='User operations')

@ns_auth.route('/register')
class UsersCollection(Resource):
    """This class creates a new user in the database"""
    @v2_api.doc(pagination_arguments)
    @v2_api.response(201, 'User created successfully')
    @v2_api.expect(user_register, validate=True)
    def post(self):
        """Creates a new user"""
        data = request.json
        errors = user_is_valid(data)
        if check_valid_email(data['email']) is None:
            response = {
                'status': 'error',
                'message': 'Not a valid email address, please try again'
            }
            return response, 403
        elif errors:
            response = {
                'status': 'error',
                'message': errors
            }
            return response, 401
        else:
            user = User(data['name'], data['username'], data['email'], data['password'])
            user.insert()
            access_token = create_access_token(user.id)
            response = {
                'status': 'success',
                'message': 'user created successfully',
                'Authorization': {
                    'access_token': access_token
                }
            }
            return response, 201

