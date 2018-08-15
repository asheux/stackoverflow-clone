from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from ..auth.errors import (
    question_doesnt_exists,
    answer_doesnt_exists
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
        if data == []:
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

@ns.route('/<int:question_id>')
@v2_api.response(404, 'question with the given id not found')
class UserQuestionItem(Resource):
    """Single question resource"""
    @jwt_required
    @v2_api.doc('Single question resource')
    @v2_api.response(200, 'Success')
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
        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Could not fetch the question: {}'.format(e)
            }
            return response, 500

    @jwt_required
    @v2_api.doc('Delete question resource')
    @v2_api.response(200, 'Successfully deleted')
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
        else:
            Question.delete(question_id)
            response = {
                'status': 'success',
                'message': 'question deleted successfully'
            }
            return response, 200

@ns.route('/<int:question_id>/answers')
@v2_api.response(404, 'question with the given id not found')
class UserAnswerResource(Resource):
    """Single question resource"""
    @jwt_required
    @v2_api.doc('Single question resource')
    @v2_api.response(200, 'Success')
    @v2_api.expect(answers)
    def post(self, question_id):
        """Post an answer to this particular question"""
        question_doesnt_exists(question_id)
        data = request.json
        answer = data['answer']
        question = Question.get_item_by_id(question_id)
        answer = Answer(answer,
                        owner=get_jwt_identity(),
                        question=question['id']
                    )
        answer.insert()
        response = {
            'status': 'success',
            'message': 'Answer posted successfully',
            'answer': answer.toJSON()
        }
        return response, 201

@ns.route('/<int:question_id>/answers/<int:answer_id>/upvote')
@v2_api.response(404, 'answer with the given id not found')
class UpvoteAnswerResourceItem(Resource):
    """Single answer resource"""
    @jwt_required
    @v2_api.doc('Single answer resource')
    @v2_api.response(200, 'Success')
    def patch(self, answer_id, question_id):
        """This resource enables users upvote an answer to a question"""
        answer_doesnt_exists(answer_id)
        question_doesnt_exists(question_id)
        allanswers = Answer.get_all()

        for answer in allanswers:
            if answer['id'] == answer_id and \
                    answer['question'] == question_id:
                answer['votes'] += 1
                response = {
                    'status': 'success',
                    'message': 'You upvoted this answer, thanks for the feedback'
                }
                return response, 200
