from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from ..auth.errors import (
    question_doesnt_exists
)
from stackoverflow import v2_api
from ..auth.serializers import questions, Pagination, answers
from stackoverflow.api.v1.auth.parsers import pagination_arguments
from stackoverflow.api.v2.models import Question, Answer
from stackoverflow import settings

ns = v2_api.namespace('questions', description='Questions operations')

@ns.route('')
class UserQuestionsResource(Resource):
    """Question resource endpoint"""
    @jwt_required
    @v2_api.doc('Question resource')
    @v2_api.response(201, 'Successfully created')
    @v2_api.expect(questions)
    def post(self):
        """Post a new question"""
        try:
            data = request.json
            title = data['title']
            description = data['description']
            questions = Question(
                title,
                description,
                created_by=get_jwt_identity()
            )
            questions.insert()
            response = {
                'status': 'success',
                'message': 'Question posted successfully',
                'data': questions.toJSON()
            }
            return response, 201
        except Exception as e:
            response = {
                'status': 'error',
                'message': 'Cannot post a question: {}'.format(e)
            }
            return response, 500

    @jwt_required
    @v2_api.doc('Question resource')
    @v2_api.response(200, 'success')
    def get(self):
        """get all questions in the platform"""
        args = pagination_arguments.parse_args(strict=True)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        data = Question.get_all()
        paginate = Pagination(page, per_page, len(data))
        if questions == []:
            response = {
                'status': 'fail',
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
