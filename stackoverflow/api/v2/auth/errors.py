import re
from ..models import User, Question, Answer
from stackoverflow.api.restplus import api

def user_is_valid(data):
    """user error handling"""
    errors = {}
    result = User.get_one_by_field('username', data.get('username'))
    error = "The email you provided is in use by another user"
    if User.get_one_by_field(
        field='email',
        value=data.get('email')) is not None:
        errors['email'] = error
    if result is not None:
        errors['username'] = "The username you provided already exists"

    return errors

def validate_str_field(string):
    if not re.match("^[ A-Za-z0-9_-]*$", string):
        return {"message": "Invalid data for username"}, 400
    return None

def validate_password(string):
    if not re.match(r'(?=.*?[0-9])(?=.*?[A-Z])(?=.*?[a-z]).{6}', string):
        return {"message": " Password rule: 1 digit, 1 caps, 1 number and minimum of 6 chars"}, 400

def validate_username(string):
    if not re.match("^[A-Za-z0-9_-]*$", string):
        return {"message": "Name should only contain letters, numbers, underscores and dashes"}, 400
    return None

def question_doesnt_exists(id):
    """Checks if given id exists in the database"""
    if not Question.get_one_by_field('id', value=id):
        api.abort(404, "Question with id {} doesn't exist or your provided an id that does not belong to you".format(id))

def answer_doesnt_exists(id):
    """Checks if given id exists in the database"""
    if not Answer.get_one_by_field('id', value=id):
        response_obj = {
            'message': 'The answer with the given id does not exist'
        }
        return response_obj, 404

def check_valid_email(email):
    """Checks if the email provided is valid"""
    return re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', email)
