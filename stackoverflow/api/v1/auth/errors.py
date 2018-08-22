"""
Imports

"""
import re
from stackoverflow.database import questionsdb, answersdb
from stackoverflow.api.restplus import API

def user_is_valid(data):
    """user error handling"""
    from .collections import store

    resp = "The username you provided already exists"
    body = store.get_by_field(key='username', value=data.get('username')) is not None
    errors = {}
    if store.get_by_field(key='email', value=data.get('email')) is not None:
        errors['email'] = "The email you provided is in use by another user"
    if body:
        errors['username'] = resp
    return errors

def answer_doesnt_exists(answer_id):
    """return error if answer not in db"""
    if answer_id not in answersdb:
        API.abort(404, "Answer with id {} doesn't exist".format(answer_id))

def question_doesnt_exists(question_id):
    """Checks if given id exists in the database"""
    if question_id not in questionsdb:
        result = "Question with id {} doesn't exist".format(question_id)
        API.abort(404, result)

def check_valid_email(email):
    """Checks if the email provided is valid"""
    return re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', email)
