from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from ..models import User, BlackListToken
from stackoverflow.database import usersdb, blacklistdb
from .errors import user_is_valid, check_valid_email

class UserStore:
    """The class controls the adding and fetching a user in the database"""

    def __init__(self):
        """Initializes the counter id"""
        self.counter = 1

    def create_user(self, data):
        """Creates a new user and adds the user in the database"""
        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password']
        errors = user_is_valid(data)

        if check_valid_email(email) is None:
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
            user = User(name, username, email, password)
            you_id = username + '00%d' % self.counter
            usersdb[you_id] = user.toJSON()
            self.counter += 1
            access_token = create_access_token(username)
            refresh_token = create_refresh_token(username)
            response = {
                'status': 'success',
                'message': 'Successfully registered',
                'your ID': self.get_the_user_id(),
                'Authorization': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }
            return response, 201


    def get_user(self, user_id):
        """Gets a single user in the database by a given id"""
        data = self.get_all_users()
        return data[user_id]

    def get_the_user_id(self):
        """Gets the last added user's id from the database"""
        return list(usersdb.keys())[-1]

    def get_all_users(self):
        """Gets all the available users from the database"""
        return usersdb

    def get_by_field(self, key, value):
        """Gets a user by a given field"""
        if self.get_all_users() is None:
            return {}
        for item in self.get_all_users().values():
            if item[key] == value:
                return item

    def is_admin(self):
        """
        To check if the user is an administrator
        :return:
        """
        return True

    def update_user(self, user_id, data):
        """Updates or modifies a given user by id"""
        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password']
        user = User(name, username, email, password)
        usersdb[user_id] = user.toJSON()

        response = {
            'status': 'success',
            'message': 'user updated successfully',
            'data': user.toJSON()
        }
        return response, 200

    def save_token(self, token):
        """Saves the blacklisted token in the database"""
        blacklist_token = BlackListToken(jti=token)
        try:
            # insert the token in database
            blacklistdb[self.counter] = blacklist_token.toJSON()
            self.counter += 1
            print(blacklistdb)
        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Could not save'.format(e)
            }
            return response, 500
