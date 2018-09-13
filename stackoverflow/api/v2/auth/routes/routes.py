"""
Imports

"""
import re
import logging
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_restplus import Resource, cors
from flask_jwt_extended import (
    jwt_required,
    get_raw_jwt,
    get_jwt_identity,
    create_access_token
)
from stackoverflow import V2_API
from stackoverflow.api.v2.auth.serializers import (
    REGISTER,
    LOGIN
)
from stackoverflow.api.v2.models import User, BlackList
from ..errors import (
    check_valid_email,
    user_is_valid,
    validate_username,
    validate_str_field,
    validate_password
)

FLASK_BCRYPT = Bcrypt()
LOG = logging.getLogger(__name__)
NS_AUTH = V2_API.namespace('auth', description='Authentication operations')
NS = V2_API.namespace('users', description='User operations')


@NS_AUTH.route('/register')
class UsersCollection(Resource):
    """This class creates a new user in the database"""
    @cors.crossdomain(origin='*')
    @V2_API.response(201, 'User created successfully')
    @V2_API.expect(REGISTER, validate=True)
    def post(self):
        """Creates a new user"""
        data = request.json
        invalid_email = 'Not a valid email address, please try again'
        errors = user_is_valid(data)
        if validate_str_field(data['name']):
            return validate_str_field(data['name'])
        if validate_username(data['username']):
            return validate_username(data['username'])
        if validate_password(data['password']):
            return validate_password(data['password'])
        if data['email'] == '':
            return jsonify({'message': {'email':'Email field cannot be empty!'}})
        if check_valid_email(data['email']) is None:
            response = {'message': {'email': invalid_email}}
            return jsonify(response), 403
        if errors:
            response = {'message': errors}
            return jsonify(response), 401
        user = User(data['name'], data['username'], data['email'], data['password'])
        user.insert()
        access_token = create_access_token(user.id)
        response = {
            'message': 'User created successfully',
            'access_token': access_token,
            'data': user.toJSON()
        }
        return jsonify(response), 201

@NS_AUTH.route('/login')
class UserLoginResource(Resource):
    """Login resource"""
    @cors.crossdomain(origin='*')
    @V2_API.doc('login user')
    @V2_API.response(200, 'Login successful')
    @V2_API.expect(LOGIN, validate=True)
    def post(self):
        """Logs in a user"""
        user_name_err = 'Username does not exist!'
        pass_err = 'Wrong username/password!'
        try:
            data = request.json
            user = User.get_one_by_field(field='username', value=data.get('username'))
            if not re.match("^[A-Za-z0-9_-]*$", data['username']):
                return jsonify({'message': 'Username should only be letters, numbers with underscores and dashes"'})
            if validate_username(data['username']):
                return jsonify({'message': 'Username field cannot be empty!'}), 401
            if data['password'] == '':
                return jsonify({'message': 'Password field cannot be empty!'}), 401
            if not user:
                response = {'message': user_name_err}
                return jsonify(response), 404
            elif not FLASK_BCRYPT.check_password_hash(user['password_hash'], data.get('password')):
                response = {'message': pass_err}
                return jsonify(response), 401
            response = {
                'message': 'Successfully logged in',
                'access_token': create_access_token(user['id']),
                'data': user
            }
            return jsonify(response), 200
        except Exception as error:
            response = {
                'message': 'Could not login: {}, try again'.format(error)}
            return jsonify(response), 400

@NS_AUTH.route('/logout_access')
class UserLogoutResourceAccess(Resource):
    """Logout resource"""
    @cors.crossdomain(origin='*')
    @V2_API.doc('logout user')
    @jwt_required # add jwt token based authentication
    @V2_API.response(200, 'Logout successful')
    def post(self):
        # get auth token
        """Logout a user"""
        jwt = get_raw_jwt()['jti']
        try:
            blacklist_token = BlackList(jti=jwt)
            blacklist_token.insert()
            response = {
                'message': 'Access token has been revoked, you are now logged out'
            }
            return jsonify(response), 200
        except Exception as error:
            response = {
                'message': 'could not generate access token: {}'.format(error)
            }
            return jsonify(response), 400

@NS.route('/userprofile')
class UserProfileResource(Resource):
    @cors.crossdomain(origin='*')
    @V2_API.doc('User profile')
    @V2_API.response(200, 'Success')
    @jwt_required
    def get(self):
        """Get user details"""
        user = User.get_one_by_field('id', value=get_jwt_identity())
        if user:
            response = {
                'status': 'success',
                'data': {
                    'name': user['name'],
                    'username': user['username'],
                    'email': user['email'],
                    'password': user['password_hash'],
                    'registered_on': user['registered_on']
                }
            }
            return jsonify(response), 200
        response = {
            "message": "No logged in user"
        }
        return jsonify(response), 404

@NS.route('')
class AllUsersResource(Resource):
    @cors.crossdomain(origin='*')
    @V2_API.doc('User profile')
    @V2_API.response(200, 'Success')
    @jwt_required
    def get(self):
        """Get all users"""
        users = User.get_all()
        if users:
            response = {
                'status': 'success',
                'allusers': users,
                'total': len(users)
            }
            return jsonify(response), 200
        response = {
            'message': 'there are no users'
        }
        return jsonify(response), 404
