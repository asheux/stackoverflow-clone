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

    @api.doc('Question resource')
    @api.response(200, 'success')
    def get(self):
        """get all questions for this particular user"""
        args = pagination_arguments.parse_args(strict=True)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        data = questionstore.get_all()
        paginate = Pagination(page, per_page, len(questions))
        if questions == []:
            response = {
                'message': 'There is no questions in the db'
            }
            return response, 404
        response = {
            'status': 'success',
            "page": paginate.page,
            "per_page": paginate.per_page,
            "total": paginate.total_count,
            'data': data
        }
        return response, 200

@ns.route('/questions/<int:question_id>')
@api.response(404, 'question with the given id not found')
class UserRequestItem(Resource):
    """Single user question resource"""
    @jwt_required
    @api.doc('Single question resource')
    @api.response(200, 'Success')
    def get(self, question_id):
        """Get a question by a specific user"""
        abort_if_request_doesnt_exists(question_id)
        data = questionstore.get_one(question_id)

        response = {
            'status': 'success',
            'data': data
        }
        return response, 200
