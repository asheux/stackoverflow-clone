"""
Imports

"""
from flask_restplus import fields
from stackoverflow.api.restplus import API

REGISTER_DATA = dict(
    name=fields.String(required=True, default='Paulla Mboya', description='User fullname'),
    username=fields.String(required=True, default='paulla', description='Username'),
    email=fields.String(required=True, default='paulla@gmail.com',
                        description='The user\'s email address'),
    password=fields.String(required=True, default='barryazah',
                           description='The users secret password'),
)
USER_REGISTER = API.model('Register Model', REGISTER_DATA)

HEAD = 'Flask restful app'
DESC = 'How to build a restful api in flask'
QUESTIONS_DATA = dict(
    title=fields.String(required=True, default=HEAD,
                        description='Question name'),
    description=fields.String(required=True, default=DESC,
                              description='the question description here')
)
QUESTIONS = API.model('Question Model', QUESTIONS_DATA)

ANSWERS = API.model('Answer Model', {
    'answer': fields.String(required=True, default='create a dictionary of data',
                            description='answer description')
})
