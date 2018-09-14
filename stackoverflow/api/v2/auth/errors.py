"""
Imports

"""
import re
from flask import jsonify
from stackoverflow.api.restplus import API
from ..models import User, Question, Answer

def user_is_valid(data):
    """user error handling"""
    errors = {}
    result = User.get_one_by_field('username', data.get('username'))
    error = "The email already exists"
    if User.get_one_by_field(field='email', value=data.get('email')) is not None:
        errors['email'] = error
    if result is not None:
        errors['username'] = "The username already exists"

    return errors

def validate_str_field(name):
    """Validate the user has input as string"""
    if name == '':
        return jsonify({"message": {"name":"You name field cannot be empty!"}}), 400
    return None

def validate_string_field(name):
    """Validate the user has input as string"""
    if name == '':
        return jsonify({"message": "Input field cannot be empty!"}), 400
    return None


def validate_password(string):
    """validates user has followed Password rules"""
    passerror = "Password should have 1 digit, one caps, and mix digits should "
    if string == '':
        return jsonify({'message': {'password':'Password field cannot be empty!'}})
    if not re.match(r'(?=.*?[0-9])(?=.*?[A-Z])(?=.*?[a-z]).{6}', string):
        return jsonify({
            "message": {'password': passerror}
        }), 400
    return None

def validate_username(string):
    """validate the user has input the right username format"""
    if not re.match("^[A-Za-z0-9_-]*$", string):
        return jsonify({'message': {'username': 'Username should only be letters, numbers with underscores and dashes'}})
    if string == '':
        return jsonify({'message': {'username':'Username field cannot be empty!'}})
    return None

def question_doesnt_exists(question_id):
    """Checks if given id exists in the database"""
    if not Question.get_one_by_field('id', value=question_id):
        API.abort(404, "Question with id {} doesn't exist".format(question_id))

def answer_doesnt_exists(answer_id):
    """Checks if given id exists in the database"""
    if not Answer.get_one_by_field('id', value=answer_id):
        response_obj = {
            'message': 'The answer with the given id does not exist'
        }
        return jsonify(response_obj), 404
    return None

def check_valid_email(email):
    """Checks if the email provided is valid"""
    if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", email) \
            and not re.match(r"(^[a-z0-9_.]+@[a-z0-9-]+\.[a-z]+\.[a-z]+$)", email):
        return None
    elif email.split('@'[-1])[-1].count('.') > 1:
        return None
    return re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', email)
