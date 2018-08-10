import logging
from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    create_access_token,
    get_raw_jwt
)
from ..parsers import pagination_arguments
from ..serializers import (
    user_register,
    user_login,
    Pagination
)
from stackoverflow.api.restplus import api
from ..collections import store
from ..authAPI import Auth

log = logging.getLogger(__name__)
ns_auth = api.namespace('auth', description='Authentication operations')
ns = api.namespace('users', description='User operations')

@ns_auth.route('/register')
class UsersCollection(Resource):
    """This class creates a new user in the database"""
    @api.doc(pagination_arguments)
    @api.response(201, 'User created successfully')
    @api.expect(user_register, validate=True)
    def post(self):
        """Creates a new user"""
        data = request.json
        return store.create_user(data=data)

@ns_auth.route('/login')
class UserLoginResource(Resource):
    """Login resource"""
    @api.doc('login user')
    @api.response(201, 'Login successful')
    @api.expect(user_login, validate=True)
    def post(self):
        """Logs in a user"""
        data = request.json
        return Auth.login_user(data=data)

@ns_auth.route('/logout_access')
class UserLogoutResourceAccess(Resource):
    """Logout resource"""
    @api.doc('logout user')
    @jwt_required
    @api.response(201, 'Logout successful')
    def post(self):
        # get auth token
        """Logout a user"""
        jti = get_raw_jwt()['jti']
        try:
            Auth.logout_user(jti)
            response = {
                'status': 'success',
                'message': 'Access token has been revoked, you are now logged out'
            }
            return response, 200
        except Exception as e:
            response = {
                'message': 'could not generate access token: {}'.format(e)
            }
            return response

