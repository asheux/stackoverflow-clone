from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from ..auth.collections import questionstore, answerstore
from ..auth.errors import abort_if_question_doesnt_exists
from stackoverflow.api.restplus import api
from ..auth.serializers import questions, Pagination, answers
from ..auth.parsers import pagination_arguments

ns = api.namespace('questions', description='Questions operations')

@ns.route('')
class UserQuestionsResource(Resource):
    """Question resource endpoint"""
    @jwt_required
    @api.doc('Question resource')
    @api.response(201, 'Successfully created')
    @api.expect(questions)
    def post(self):
        """Post a new question"""
        data = request.json
        return questionstore.create_question(data=data)

    @jwt_required
    @api.doc('Question resource')
    @api.response(200, 'success')
    def get(self):
        """get all questions for this particular user"""
        args = pagination_arguments.parse_args(strict=True)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        data = questionstore.get_all()
        questions = [quiz for quiz in data.values()]
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
            'data': questions
        }
        return response, 200

@ns.route('/<int:question_id>')
@api.response(404, 'question with the given id not found')
class UserRequestItem(Resource):
    """Single question resource"""
    @jwt_required
    @api.doc('Single question resource')
    @api.response(200, 'Success')
    def get(self, question_id):
        """Get a question"""
        abort_if_question_doesnt_exists(question_id)
        data = questionstore.get_one(question_id)

        response = {
            'status': 'success',
            'data': data
        }
        return response, 200

    @jwt_required
    @api.doc('Delete question resource')
    @api.response(200, 'Successfully deleted')
    def delete(self, question_id):
        """Deletes a question with the given id"""
        abort_if_question_doesnt_exists(question_id)
        my_question = questionstore.get_one(question_id)
        if my_question['created_by']['username'] != get_jwt_identity():
            response = {
                'status': 'fail',
                'message': 'You are not permitted to delete this question'
            }

            return response, 401
        else:
            questionstore.delete(question_id)
            response = {
                'status': 'success',
                'message': 'question deleted successfully'
            }
            return response, 200

@ns.route('/<int:question_id>/answers')
@api.response(404, 'question with the given id not found')
class UserAnswerResource(Resource):
    """Single question resource"""
    @jwt_required
    @api.doc('Single question resource')
    @api.response(200, 'Success')
    @api.expect(answers)
    def post(self, question_id):
        """Post an answer to this particular question"""
        data = request.json
        abort_if_question_doesnt_exists(question_id)
        return answerstore.post_answer(question_id, data)

    @jwt_required
    @api.doc('Answer resource')
    @api.response(200, 'success')
    def get(self, question_id):
        """get all answers for this particular question"""
        abort_if_question_doesnt_exists(question_id)
        args = pagination_arguments.parse_args(strict=True)
        question = questionstore.get_one(question_id)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        data = answerstore.get_all()
        answers = [answer for answer in data.values()
                   if answer['question'] == question]
        paginate = Pagination(page, per_page, len(answers))
        if answers == []:
            response = {
                'message': 'There is no questions in the db'
            }
            return response, 404
        response = {
            'status': 'success',
            "page": paginate.page,
            "per_page": paginate.per_page,
            "total": paginate.total_count,
            'data': answers
        }
        return response, 200

