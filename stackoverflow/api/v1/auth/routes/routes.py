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

@ns.route('/current')
class UserItem(Resource):
    """Show a single user item"""
    @api.response(200, 'success')
    @jwt_required
    @api.doc('user gets their details')
    def get(self):
        """Returns a logged in user's details"""
        current_user = get_jwt_identity()
        return Auth.get_logged_in_user(current_user)

@ns.route('', endpoint='all_users')
class AllUsersResource(Resource):
    """Shows a list of all users"""
    @api.doc('get list of users')
    @api.expect(pagination_arguments)
    def get(self):
        """Return list of users"""
        args = pagination_arguments.parse_args(strict=True)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        users_query = store.get_all()
        users = [user for user in users_query.values()]
        paginate = Pagination(page, per_page, len(users))
        if users_query == {}:
            response = {
                "message": "There are no users in the database yet"
            }
            return response, 404
        else:
            response = {
                'status': 'success',
                "page": paginate.page,
                "per_page": paginate.per_page,
                "total": paginate.total_count,
                "data": users
            }
            return response, 200
