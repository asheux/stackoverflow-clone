"""
Imports

"""
from flask_restplus import fields
from stackoverflow import V2_API

REGISTER = V2_API.model('Register Model', {
    'name': fields.String(required=True, default='Brian Mboya', description='User fullname'),
    'username': fields.String(required=True, default='asheuh', description='Username'),
    'email': fields.String(required=True, default='asheuh@gmail.com',
                           description='The user\'s email address'),
    'password': fields.String(required=True, default='mermaid',
                              description='The users secret password'),
})

DATA = {
    'username': fields.String(required=True, default='asheuh', description='Your username'),
    'password': fields.String(required=True, default='mermaid', description='Your password'),
}
LOGIN = V2_API.model('Login Model', DATA)
D_HEAD = 'Django restful api'
DESC_BODY = 'How to write serializers'
QUESTIONS = V2_API.model('Question Model', {
    'title': fields.String(required=True, default=D_HEAD, description='Request name'),
    'description': fields.String(required=True, default=DESC_BODY,
                                 description='question description')
})

ANSWERS = V2_API.model('Answer Model', {
    'answer': fields.String(required=True, default='create a dictionary of data',
                            description='answer description')
})
