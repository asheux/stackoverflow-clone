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
    user_register
)
from stackoverflow.api.restplus import api
from ..collections import store

log = logging.getLogger(__name__)
ns_auth = api.namespace('auth', description='Authentication operations')
ns = api.namespace('user', description='User operations')

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
