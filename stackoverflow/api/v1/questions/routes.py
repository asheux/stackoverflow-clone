from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from ..auth.collections import questionstore, answerstore
from ..auth.errors import (
    abort_if_question_doesnt_exists,
    abort_if_answer_doesnt_exists
)
from stackoverflow.api.restplus import api
from ..auth.serializers import questions, Pagination, answers
from ..auth.parsers import pagination_arguments
from stackoverflow import settings

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
        """get all questions in the platform"""
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
class UserQuestionItem(Resource):
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
                'message': 'There are no answers in the db for this question'
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

@ns.route('/<int:question_id>/answers/<int:answer_id>/accept')
@api.response(404, 'answer with the given id not found')
class AcceptAnswerResourceItem(Resource):
    """Single answer resource"""
    @jwt_required
    @api.doc('Single answer resource')
    @api.response(200, 'Success')
    def patch(self, answer_id, question_id):
        """This resource enables users accept an answer to their question"""
        allquiz = questionstore.get_all()
        allanswers = answerstore.get_all()
        questions = [quiz for quiz in allquiz.values()
                     if quiz['created_by']['username'] == get_jwt_identity()]
        answers = [answer for answer in allanswers.values()
                   if answer['question'] == answerstore.get_a_user_quiz(questions)]

        for answer in answers:
            if answer['question']['id'] != question_id:
                response = {
                    'status': 'error',
                    'message': 'Question with the provided id does not exist'
                }
                return response, 404
            elif answer['id'] != answer_id:
                response = {
                    'status': 'error',
                    'message': 'Answer with the given id doesnt exists'
                }
                return response, 404
            elif answer['accepted'] != False:
                response = {
                    'status': 'fail',
                    'message': 'This answer has been accepted already'
                }
                return response, 403
            answer['accepted'] = settings.ACCEPT
            response = {
                'status': 'success',
                'message': 'Answer accepted'
            }
            return response, 200

@ns.route('/<int:question_id>/answers/<int:answer_id>/upvote')
@api.response(404, 'answer with the given id not found')
class UpvoteAnswerResourceItem(Resource):
    """Single answer resource"""
    @jwt_required
    @api.doc('Single answer resource')
    @api.response(200, 'Success')
    def patch(self, answer_id, question_id):
        """This resource enables users upvote an answer to a question"""
        abort_if_answer_doesnt_exists(answer_id)
        abort_if_question_doesnt_exists(question_id)
        allanswers = answerstore.get_all()
        answers = [answer for answer in allanswers.values()]

        for answer in answers:
            if answer['id'] == answer_id:
                answer['votes'] += 1
                response = {
                    'status': 'success',
                    'message': 'Your vote was recorded'
                }
                return response, 200
