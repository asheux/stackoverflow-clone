from flask_bcrypt import Bcrypt
from flask import request
from flask_jwt_extended import (
    create_access_token
)
from .collections import store

flask_bcrypt = Bcrypt()

class Auth:
    """The class handles all authentications"""
    @staticmethod
    def login_user(data):
        """Login authentication"""
        try:
            data = request.json
            user = store.get_by_field(key='username', value=data.get('username'))
            if not user:
                response = {
                    'status': 'fail',
                    'message': 'The username you provided does not exist'}
                return response, 404
            elif not flask_bcrypt.check_password_hash(user['password_hash'], data.get('password')):
                response = {
                    'status': 'fail',
                    'message': 'The password you provided did not match the database password'}
                return response, 401
            else:
                response = {
                    'status': 'success',
                    'message': 'Successfully logged in as {}'.format(user['name']),
                    'Authorization': {
                        'access_token': create_access_token(user['username'])}}
                return response, 201
        except Exception as e:
            response = {
                'message': 'Could not login: {}, try again.'.format(e)}
            return response, 500

    @staticmethod
    def logout_user(data):
        """Logout authentication"""
        return store.save_token(data)


    @staticmethod
    def get_logged_in_user(identity):
        """Get the currently logged in user"""
        # get the auth token
        user = store.get_by_field(key='username', value=identity)
        if user is not None:
            response_obj = {
                'status': 'success',
                'data': {
                    'name': user['name'],
                    'username': user['username'],
                    'email': user['email'],
                    'password': user['password_hash'],
                    'registered_on': user['registered_on']
                }
            }
            return response_obj, 200
        else:
            response_obj = {
                'status': 'fail',
                'message': 'user is none'
            }
            return response_obj, 404
