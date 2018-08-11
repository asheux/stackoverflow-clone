from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from ..auth.collections import questionstore
from ..auth.errors import abort_if_request_doesnt_exists
from stackoverflow.api.restplus import api
from ..auth.serializers import questions, Pagination
from ..auth.parsers import pagination_arguments

ns = api.namespace('user', description='User operations')

@ns.route('/questions')
class UserQuestionsResource(Resource):
    """Question resource endpoint"""
    @jwt_required
    @api.doc('Question resource')
    @api.response(201, 'Successfully created')
    @api.expect(questions)
    def post(self):
        """Creates a new question"""
        data = request.json
        return questionstore.create_question(data=data)

