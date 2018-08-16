import re
from stackoverflow.database import questionsdb, answersdb
from stackoverflow.api.restplus import api

def user_is_valid(data):
    """user error handling"""
    from .collections import store

    errors = {}
    if store.get_by_field(key='email', value=data.get('email')) is not None:
        errors['email'] = "The email you provided is in use by another user"
    if store.get_by_field(key='username', value=data.get('username')) is not None:
        errors['username'] = "The username you provided already exists"

    return errors

def answer_doesnt_exists(id):
    """return error if answer not in db"""
    if id not in answersdb:
        api.abort(404, "Answer with id {} doesn't exist".format(id))

def question_doesnt_exists(id):
    """Checks if given id exists in the database"""
    if id not in questionsdb:
        api.abort(404, "Question with id {} doesn't exist".format(id))

def check_valid_email(email):
    """Checks if the email provided is valid"""
    return re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', email)
