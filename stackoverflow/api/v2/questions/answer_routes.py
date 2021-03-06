"""
Imports

"""
import heapq
from flask import request, jsonify
from flask_restplus import Resource, cors
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from stackoverflow.api.v2.models import Question, Answer
from stackoverflow import V2_API, settings
from ..auth.errors import (
    question_doesnt_exists,
    answer_doesnt_exists
)
from ..auth.serializers import ANSWERS

NS = V2_API.namespace('questions', description='Questions operations')

def answer_dict(my_list):
    """Get an item from a list"""
    for i in my_list:
        return i

@NS.route('/<int:question_id>/answers')
@V2_API.response(404, 'question with the given id not found')
class UserAnswerResource(Resource):
    """Single question resource"""
    @cors.crossdomain(origin='*')
    @jwt_required # add jwt token based authentication
    @V2_API.doc('Single question resource')
    @V2_API.response(200, 'Success')
    @V2_API.expect(ANSWERS)
    def post(self, question_id):
        """Post an answer to this particular question"""
        question_doesnt_exists(question_id)
        data = request.json
        answer = data['answer']
        if answer == '':
            response = {
                'message': 'Cannot post empty answer'
            }
            return jsonify(response)

        question = Question.get_item_by_id(question_id)
        answers = Answer.get_one_by_field('answer', data['answer'])

        if answers is not None:
            response_obj = {
                'message': 'Same answer exist already, please vote on it'
            }
            return jsonify(response_obj), 409
        answer = Answer(answer,
                        owner=get_jwt_identity(),
                        question=question['id']
                    )
        answer.insert()
        question['answers'] += 1
        Question.update('answers', question['answers'], question_id)
        response = {
            'message': 'Answer posted successfully',
            'answer': answer.toJSON()
        }
        return jsonify(response), 201

    @cors.crossdomain(origin='*')
    @jwt_required
    @V2_API.doc('All answers for this question')
    @V2_API.response(200, 'success')
    def get(self, question_id):
        """Gets all the answers for this particular question"""
        question_doesnt_exists(question_id)
        question = Question.get_item_by_id(question_id)
        data = Answer.get_all()
        answers = [answer for answer in data
                   if answer['question'] == question['id']]
        if answers == []:
            response = {
                'message': 'There are answers for this question'
            }
            return jsonify(response), 404
        response = {
            'total': len(answers),
            'data': answers
        }
        return jsonify(response), 200

@NS.route('/<int:question_id>/answers/<int:answer_id>/upvote')
@V2_API.response(404, 'answer with the given id not found')
class UpvoteAnswerResourceItem(Resource):
    """Single answer resource"""
    @cors.crossdomain(origin='*')
    @jwt_required # add jwt token based authentication
    @V2_API.doc('Single answer resource')
    @V2_API.response(200, 'Success')
    def patch(self, answer_id, question_id):
        """This resource enables users upvote an answer to a question"""
        answer_doesnt_exists(answer_id)
        question_doesnt_exists(question_id)
        allanswers = Answer.get_all()

        for answer in allanswers:
            if answer['id'] == answer_id and \
                    answer['question'] == question_id:
                answer['votes'] += 1
                Answer.update('votes', answer['votes'], answer_id)
                response = {
                    'message': 'You upvoted this answer, thanks for the feedback'
                }
                return jsonify(response), 200
            response = {
                'message': 'the answer given does not exist'
            }
            return jsonify(response), 404

@NS.route('/<int:question_id>/answers/<int:answer_id>/downvote')
@V2_API.response(404, 'answer with the given id not found')
class DownvoteAnswerResourceItem(Resource):
    """Single answer resource"""
    @cors.crossdomain(origin='*')
    @jwt_required # add jwt token based authentication
    @V2_API.doc('Single answer resource')
    @V2_API.response(200, 'Success')
    def patch(self, answer_id, question_id):
        """This resource enables users down vote an answer to a question"""
        answer_doesnt_exists(answer_id)
        question_doesnt_exists(question_id)
        allanswers = Answer.get_all()

        for answer in allanswers:
            if answer['id'] == answer_id and \
                    answer['question'] == question_id:
                answer['votes'] -= 1
                Answer.update('votes', answer['votes'], answer_id)
                response = {
                    'message': 'You down voted this answer, thanks for the feedback'
                }
                return jsonify(response), 200
            response = {
                'message': 'No answer with that id'
            }
            return jsonify(response), 404

@NS.route('/<int:question_id>/answers/<int:answer_id>/accept')
@V2_API.response(404, 'answer with the given id not found')
class AcceptAnswerResourceItem(Resource):
    """Single answer resource"""
    @cors.crossdomain(origin='*')
    @jwt_required # add jwt token based authentication
    @V2_API.doc('Single answer resource')
    @V2_API.response(200, 'Success')
    def patch(self, answer_id, question_id):
        """This resource enables users accept an answer to their question"""
        question_doesnt_exists(question_id)
        answer_doesnt_exists(answer_id)
        allquiz = Question.get_all()
        allanswers = Answer.get_all()
        questions = [quiz for quiz in allquiz
                     if quiz['created_by'] == get_jwt_identity()]
        answers = [answer for answer in allanswers
                   if answer['question'] == answer_dict(questions)['id']]
        if answers == []:
            response = {
                'message': 'There are no answers for this question'}
            return jsonify(response), 404
        for my_answer in answers:
            if my_answer['accepted'] != False:
                response_obj = {
                    'message': 'This answers has already been accepted'
                }
                return jsonify(response_obj), 400
            elif my_answer['id'] == answer_id \
                    and my_answer['question'] == question_id:
                my_answer['accepted'] = settings.ACCEPT
                Answer.update('accepted', my_answer['accepted'], answer_id)
                response = {
                    'message': 'Answer accepted',
                    'data': my_answer}
                return jsonify(response), 200
            response_obj = {
                'message': 'Could not perform action, check the id you provided'}
            return jsonify(response_obj), 404
@NS.route('/myquestions')
class UserQuestions(Resource):
    """User questions posted"""
    @cors.crossdomain(origin='*')
    @jwt_required # add jwt token based authentication
    @V2_API.doc('All questions for user')
    @V2_API.response(200, 'Success')
    def get(self):
        """Get all questions for this user"""
        data = Question.get_all()
        myquestions = [quezes for quezes in data
                       if quezes['created_by'] == get_jwt_identity()]
        if myquestions == []:
            response = {
                'message': 'There are no questions in the db for you'
            }
            return jsonify(response), 404
        response = {
            'total': len(myquestions),
            'data': myquestions
        }
        return jsonify(response), 200

@NS.route('/mostanswers')
class UserQuestionAnswer(Resource):
    """Most answered question"""
    @cors.crossdomain(origin='*')
    @jwt_required
    @V2_API.doc('Question with most answers')
    @V2_API.response(200, 'Success')
    def get(self):
        """Get the question with the most answers"""
        questions = Question.get_all()
        myquestions = [question for question in questions
                       if question['created_by'] == get_jwt_identity()]
        list_num = [question['answers'] for question in questions
                    if question['created_by'] == get_jwt_identity()]
        if questions == []:
            response = {
                'message': 'There are no questions'
            }
            return jsonify(response), 404
        most_answer = heapq.nlargest(2, list_num)
        print(most_answer)
        for i in most_answer:
            if i < 0:
                response = {
                    'message': 'Your question has no answers'
                }
                return jsonify(response)
        all_quiz = [quiz for quiz in myquestions
                    if quiz['answers'] in most_answer and quiz['answers'] > 0]
        response = {
            'total': len(all_quiz),
            'data': all_quiz
        }
        return jsonify(response), 200

@NS.route('/search/<string:search_item>')
class UserSearchQuestion(Resource):
    """Search resource"""
    @cors.crossdomain(origin='*')
    @jwt_required
    @V2_API.doc('Searching a question in the platform')
    @V2_API.response(200, 'success')
    def get(self, search_item):
        """Search question resource"""
        Question.transform_for_search()
        result = Question.fts_search_query(search_item)
        if result == []:
            response = {
                'message': 'No results for your search'
            }
            return jsonify(response), 404
        response = {
            'total': len(result),
            'data': result
        }
        return jsonify(response), 200
