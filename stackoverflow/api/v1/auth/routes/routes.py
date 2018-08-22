"""
Imports

"""
import logging
from flask import request
from flask_restplus import Resource, fields
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_raw_jwt
)
from stackoverflow.api.restplus import API
from ..serializers import (
    USER_REGISTER
)
from ..collections import store
from ..authAPI import Auth

LOG = logging.getLogger(__name__)
NS_AUTH = API.namespace('auth', description='Authentication operations')
NS = API.namespace('users', description='User operations')

USER_LOGIN = API.model('Login Model',
                       dict(username=fields.String(required=True, default='asheuh',
                                                   description='Your username'),
                            password=fields.String(required=True, default='mermaid',
                                                   description='Your password'),))

@NS_AUTH.route('/register')
class UsersCollection(Resource):
    """This class creates a new user in the database"""
    @API.response(201, 'User created successfully')
    @API.expect(USER_REGISTER, validate=True)
    def post(self):
        """Creates a new user"""
        data = request.json
        return store.create_user(result=data)

@NS_AUTH.route('/login')
class UserLoginResource(Resource):
    """Login resource"""
    @API.doc('login user')
    @API.response(201, 'Login successful')
    @API.expect(USER_LOGIN, validate=True)
    def post(self):
        """Logs in a user"""
        data = request.json
        return Auth.login_user(data=data)

@NS_AUTH.route('/logout_access')
class UserLogoutResourceAccess(Resource):
    """Logout resource"""
    @API.doc('logout user')
    @jwt_required
    @API.response(201, 'Logout successful')
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
            return response, 500

@NS.route('/current')
class UserItem(Resource):
    """Show a single user item"""
    @API.response(200, 'success')
    @jwt_required
    @API.doc('user gets their details')
    def get(self):
        """Returns a logged in user's details"""
        current_user = get_jwt_identity()
        return Auth.get_logged_in_user(current_user)

@NS.route('', endpoint='all_users')
class AllUsersResource(Resource):
    """Shows a list of all users"""
    @API.doc('get list of users')
    def get(self):
        """Return list of users"""
        users_query = store.get_all()
        users = [user for user in users_query.values()]
        if users_query == {}:
            response = {
                "message": "There are no users in the database yet"
            }
            return response, 404
        response = {
            'status': 'success',
            'total': len(users),
            "data": users
        }
        return response, 200
