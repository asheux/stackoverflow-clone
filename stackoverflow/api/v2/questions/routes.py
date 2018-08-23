"""
Imports

"""

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from stackoverflow import V2_API
from stackoverflow.api.v2.models import Question
from ..auth.errors import (
    question_doesnt_exists
)
from ..auth.serializers import QUESTIONS

NS = V2_API.namespace('questions', description='Questions operations')

def get_quiz_dict(list_obj):
    """Get on item in a list"""
    for item in list_obj:
        return item

@NS.route('')
class UserQuestionsResource(Resource):
    """Question resource endpoint"""
    @jwt_required # add jwt token based authentication
    @V2_API.doc('Question resource')
    @V2_API.response(201, 'Successfully created')
    @V2_API.expect(QUESTIONS)
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
        except Exception as error:
            response = {
                'status': 'error',
                'message': 'Cannot post a question: {}'.format(error)
            }
            return response, 400

    @jwt_required # add jwt token based authentication
    @V2_API.doc('Question resource')
    @V2_API.response(200, 'success')
    def get(self):
        """get all questions in the platform"""
        data = Question.get_all()
        if data == []:
            response = {
                'status': 'fail',
                'message': 'There is no questions in the db'
            }
            return response, 404
        response = {
            'status': 'success',
            'total': len(data),
            'data': data
        }
        return response, 200

@NS.route('/<int:question_id>')
@V2_API.response(404, 'question with the given id not found')
class UserQuestionItem(Resource):
    """Single question resource"""
    @jwt_required # add jwt token based authentication
    @V2_API.doc('Single question resource')
    @V2_API.response(200, 'Success')
    def get(self, question_id):
        """Get a question"""
        question_doesnt_exists(question_id)
        try:
            question = Question.get_item_by_id(question_id)
            question_doesnt_exists(question_id)
            response = {
                'status': 'success',
                'data': question
            }
            return response, 200
        except Exception as error:
            response = {
                'status': 'fail',
                'message': 'Could not fetch the question: {}'.format(error)
            }
            return response, 400

    @jwt_required # add jwt token based authentication
    @V2_API.doc('Delete question resource')
    @V2_API.response(200, 'Successfully deleted')
    def delete(self, question_id):
        """Deletes a question with the given id"""
        question_doesnt_exists(question_id)
        my_question = Question.get_item_by_id(question_id)
        if my_question['created_by'] != get_jwt_identity():
            response = {
                'status': 'fail',
                'message': 'You are not permitted to delete this question'
            }
            return response, 401
        Question.delete(question_id)
        response = {
            'status': 'success',
            'message': 'question deleted successfully'
        }
        return response, 200
