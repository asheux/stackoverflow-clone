from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from ..auth.collections import questionstore, answerstore
from ..auth.errors import (
    question_doesnt_exists,
    answer_doesnt_exists
)
from stackoverflow.api.restplus import api
from ..auth.serializers import questions, answers
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
        data = questionstore.get_all()
        questions = [quiz for quiz in data.values()]
        if questions == []:
            response = {
                'status': 'fail',
                'message': 'There is no questions in the db'
            }
            return response, 404
        response = {
            'status': 'success',
            "total": len(questions),
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
        question_doesnt_exists(question_id)
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
        question_doesnt_exists(question_id)
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
        question_doesnt_exists(question_id)
        data = request.json
        result = answerstore.get_by_field(key='answer', value=data['answer'])
        for i in result:
            if i is not None and i['accepted'] == False:
                response = {
                    'status': 'fail',
                    'message': 'This answer was provided and is not accepted yet, please react on it'
                }
                return response, 500
        return answerstore.post_answer(question_id, data)

    @jwt_required
    @api.doc('Answer resource')
    @api.response(200, 'success')
    def get(self, question_id):
        """get all answers for this particular question"""
        question_doesnt_exists(question_id)
        question = questionstore.get_one(question_id)
        data = answerstore.get_all()
        answers = [answer for answer in data.values()
                   if answer['question'] == question_id]
        if answers == []:
            response = {
                'message': 'There are no answers in the db for this question'
            }
            return response, 404
        response = {
            'status': 'success',
            "total": len(answers),
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
                   if answer['question'] == answerstore.get_a_user_quiz(questions)['id']]
        for answer in answers:
            if answer['question'] != question_id:
                response = {
                    'message': 'Question with the provided id does not exist'}
                return response, 404
            elif answer['id'] != answer_id:
                response = {
                    'message': 'Answer with the given id doesnt exists'}
                return response, 404
            elif answer['accepted'] != False:
                response = {
                    'message': 'This answer has been accepted already'}
                return response, 403
            answer['accepted'] = settings.ACCEPT
            response = {
                'status': 'success',
                'message': 'Answer accepted'}
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
        answer_doesnt_exists(answer_id)
        question_doesnt_exists(question_id)
        allanswers = answerstore.get_all()
        answers = [answer for answer in allanswers.values()]

        for answer in answers:
            if answer['id'] == answer_id:
                answer['votes'] += 1
                response = {
                    'status': 'success',
                    'message': 'You upvoted this answer, thanks for the feedback'
                }
                return response, 200

@ns.route('/<int:question_id>/answers/<int:answer_id>/downvote')
@api.response(404, 'answer with the given id not found')
class DownvoteAnswerResourceItem(Resource):
    """Single answer resource"""
    @jwt_required
    @api.doc('Single answer resource')
    @api.response(200, 'Success')
    def patch(self, answer_id, question_id):
        """This resource enables users upvote an answer to a question"""
        answer_doesnt_exists(answer_id)
        question_doesnt_exists(question_id)
        allanswers = answerstore.get_all()
        answers = [answer for answer in allanswers.values()]

        for answer in answers:
            if answer['id'] == answer_id:
                answer['votes'] -= 1
                response = {
                    'status': 'success',
                    'message': 'You down voted this answer, thanks for the feedback'
                }
                return response, 200
