from flask_jwt_extended import (
    create_access_token
)
from ..models import User, BlackListToken, Question, Answer
from stackoverflow.database import (
    db,
    blacklistdb,
    questionsdb,
    get_current_user,
    answersdb
)
from .errors import user_is_valid, check_valid_email

class UserStore:
    """The class controls the adding and fetching a user in the database"""

    def __init__(self):
        """Initializes the counter id"""
        self.counter = 1

    def create_user(self, data):
        """Creates a new user and adds the user in the database"""
        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password']
        errors = user_is_valid(data)

        if check_valid_email(email) is None:
            response = {
                'status': 'error',
                'message': 'Not a valid email address, please try again'
            }
            return response, 403

        elif errors:
            response = {
                'status': 'error',
                'message': errors
            }
            return response, 401
        else:
            user = User(name, username, email, password)
            user.id = self.counter
            db[self.counter] = user.toJSON()
            self.counter += 1
            access_token = create_access_token(username)
            response = {
                'status': 'success',
                'message': 'Successfully registered',
                'data': user.toJSON(),
                'Authorization': {
                    'access_token': access_token
                }
            }
            return response, 201


    def get_item(self, id):
        """Gets a single user in the database by a given id"""
        data = self.get_all()
        return data[id]

    def get_all(self):
        """Gets all the available users from the database"""
        return db

    def get_by_field(self, key, value):
        """Gets a user by a given field"""
        if self.get_all() is None:
            return {}
        for item in self.get_all().values():
            if item[key] == value:
                return item

    def save_token(self, token):
        """Saves the blacklisted token in the database"""
        blacklist_token = BlackListToken(jti=token)
        try:
            # insert the token in database
            blacklistdb[self.counter] = blacklist_token.toJSON()
            self.counter += 1
        except Exception as e:
            response = {
                'status': 'fail',
                'message': 'Could not save'.format(e)
            }
            return response, 500

class QuestionStore:
    def __init__(self):
        self.index = 1

    def create_question(self, data):
        title = data['title']
        description = data['description']
        questions = Question(
            title,
            description,
            created_by=get_current_user()
        )
        questions.id = self.index
        questionsdb[self.index] = questions.toJSON()
        self.index += 1

        response = {
            'status': 'success',
            'message': 'Question posted successfully',
            'data': questions.toJSON()
        }
        return response, 201

    def get_all(self):
        """Gets all questions in the database"""
        return questionsdb

    def get_by_field(self, key, value):
        """Gets a question by a given field"""
        if self.get_all() is None:
            return {}
        for item in self.get_all().values():
            if item[key] == value:
                return item

    def get_one(self, id):
        """Gets a single question by a given request id"""
        data = self.get_all()
        return data[id]

    def delete(self, id):
        """Deletes a particular question for a user"""
        data = self.get_all()
        del data[id]

class AnswerStore:
    def __init__(self):
        self.index = 1

    def post_answer(self, id,  data):
        questionstore = QuestionStore()
        answer = data['answer']
        question = questionstore.get_one(id)
        answer = Answer(answer,
                        owner=get_current_user(),
                        question=question
                    )
        answer.id = self.index
        answersdb[self.index] = answer.toJSON()
        self.index += 1

        response = {
            'status': 'success',
            'message': 'Answer posted successfully',
            'answer': answer.toJSON()
        }
        return response, 201

    def get_all(self):
        """Get all the answer to a question"""
        return answersdb

    def get_one(self, id):
        """Gets a single answer to a question"""
        data = self.get_all()
        return data[id]

    def get_a_user_quiz(self, my_list):
        for item in my_list:
            return item
