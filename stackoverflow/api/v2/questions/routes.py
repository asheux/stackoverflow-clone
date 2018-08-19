import heapq
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
from ..auth.serializers import questions, answers
from stackoverflow.api.v2.models import Question, Answer
from stackoverflow import settings

ns = v2_api.namespace('questions', description='Questions operations')

def get_quiz_dict(list_obj):
    for item in list_obj:
        return item

@ns.route('')
class UserQuestionsResource(Resource):
    """Question resource endpoint"""
    @jwt_required # add jwt token based authentication
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

    @jwt_required # add jwt token based authentication
    @v2_api.doc('Question resource')
    @v2_api.response(200, 'success')
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

@ns.route('/<int:question_id>')
@v2_api.response(404, 'question with the given id not found')
class UserQuestionItem(Resource):
    """Single question resource"""
    @jwt_required # add jwt token based authentication
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

    @jwt_required # add jwt token based authentication
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
    @jwt_required # add jwt token based authentication
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
        question['answers'] += 1
        Question.updatequestion(question['answers'], question_id)
        response = {
            'status': 'success',
            'message': 'Answer posted successfully',
            'answer': answer.toJSON()
        }
        return response, 201

    @jwt_required
    @v2_api.doc('All answers for this question')
    @v2_api.response(200, 'success')
    def get(self, question_id):
        """Gets all the answers for this particular question"""
        question_doesnt_exists(question_id)
        question = Question.get_item_by_id(question_id)
        data = Answer.get_all()
        answers = [answer for answer in data
                   if answer['question'] == question_id]
        if answers == []:
            response = {
                'status': 'fail',
                'message': 'There are answers in the database for this question'
            }
            return response, 404
        response = {
            'status': 'success',
            'total': len(answers),
            'data': answers
        }
        return response, 200

@ns.route('/<int:question_id>/answers/<int:answer_id>/upvote')
@v2_api.response(404, 'answer with the given id not found')
class UpvoteAnswerResourceItem(Resource):
    """Single answer resource"""
    @jwt_required # add jwt token based authentication
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
                Answer.voteandupdate(answer['votes'], answer_id)
                response = {
                    'status': 'success',
                    'message': 'You upvoted this answer, thanks for the feedback'
                }
                return response, 200

@ns.route('/<int:question_id>/answers/<int:answer_id>/downvote')
@v2_api.response(404, 'answer with the given id not found')
class DownvoteAnswerResourceItem(Resource):
    """Single answer resource"""
    @jwt_required # add jwt token based authentication
    @v2_api.doc('Single answer resource')
    @v2_api.response(200, 'Success')
    def patch(self, answer_id, question_id):
        """This resource enables users down vote an answer to a question"""
        answer_doesnt_exists(answer_id)
        question_doesnt_exists(question_id)
        allanswers = Answer.get_all()

        for answer in allanswers:
            if answer['id'] == answer_id and \
                    answer['question'] == question_id:
                answer['votes'] -= 1
                Answer.voteandupdate(answer['votes'], answer_id)
                response = {
                    'status': 'success',
                    'message': 'You down voted this answer, thanks for the feedback'
                }
                return response, 200

@ns.route('/<int:question_id>/answers/<int:answer_id>/accept')
@v2_api.response(404, 'answer with the given id not found')
class AcceptAnswerResourceItem(Resource):
    """Single answer resource"""
    @jwt_required # add jwt token based authentication
    @v2_api.doc('Single answer resource')
    @v2_api.response(200, 'Success')
    def patch(self, answer_id, question_id):
        """This resource enables users accept an answer to their question"""
        allquiz = Question.get_all()
        allanswers = Answer.get_all()
        questions = [quiz for quiz in allquiz
                     if quiz['created_by'] == get_jwt_identity()]
        answers = [answer for answer in allanswers
                   if answer['question'] == get_quiz_dict(questions)['id']]
        if answers == []:
            response = {
                'status': 'fail',
                'message': 'There are no answers for this question'
            }
            return response, 404

        for answer in answers:
            if answer['question'] != question_id:
                response_obj = {
                    'status': 'fail',
                    'message': 'The question with that id does not exist'
                }
                return response_obj, 404
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
            Answer.accepteandupdate(answer['accepted'], answer_id)
            response = {
                'status': 'success',
                'message': 'Answer accepted'
            }
            return response, 200
@ns.route('/myquestions')
class UserQuestions(Resource):
    @jwt_required # add jwt token based authentication
    @v2_api.doc('All questions for user')
    @v2_api.response(200, 'Success')
    def get(self):
        """Get all questions for this user"""
        data = Question.get_all()
        myquestions = [quezes for quezes in data
                       if quezes['created_by'] == get_jwt_identity()]
        if myquestions == []:
            response = {
                'status': 'fail',
                'message': 'There are no questions in the db for you'
            }
            return response, 404
        response = {
            'status': 'success',
            'total': len(myquestions),
            'data': myquestions
        }
        return response, 200

@ns.route('/mostanswers')
class UserQuestionAnswer(Resource):
    @jwt_required
    @v2_api.doc('Question with most answers')
    @v2_api.response(200, 'Success')
    def get(self):
        """Get the question with the most answers"""
        questions = Question.get_all()
        list_num = [question['answers'] for question in questions]
        if questions == []:
            response = {
                'status': 'fail',
                'message': 'There are no questions'
            }
            return response, 404
        most_answer = heapq.nlargest(2, list_num)
        all_quiz = [quiz for quiz in questions
                    if quiz['answers'] in most_answer]
        response = {
            'status': 'success',
            'total': len(all_quiz),
            'data': all_quiz
        }
        return response, 200

@ns.route('/search/<string:search_item>')
class UserSearchQuestion(Resource):
    @jwt_required
    @v2_api.doc('Searching a question in the platform')
    @v2_api.response(200, 'success')
    def get(self, search_item):
        """Search question resource"""
        Question.transform_for_search()
        result = Question.fts_search_query(search_item)
        if result == []:
            response = {
                'status': 'fail',
                'message': 'No results for your search'
            }
            return response, 404
        response = {
            'status': 'success',
            'total': len(result),
            'data': result
        }
        return response, 200
