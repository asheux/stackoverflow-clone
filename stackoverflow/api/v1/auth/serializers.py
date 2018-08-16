from flask_restplus import fields
from stackoverflow.api.restplus import api

user_register = api.model('Register Model', {
    'name': fields.String(required=True, default='Brian Mboya', description='User fullname'),
    'username': fields.String(required=True, default='asheuh', description='Username'),
    'email': fields.String(required=True, default='asheuh@gmail.com', description='The user\'s email address'),
    'password': fields.String(required=True, default='mermaid', description='The users secret password'),
})

user_login = api.model('Login Model', {
    'username': fields.String(required=True, default='asheuh', description='Your username'),
    'password': fields.String(required=True, default='mermaid', description='Your password'),
})

questions = api.model('Question Model', {
    'title': fields.String(required=True, default='Django restful api', description='Request name'),
    'description': fields.String(required=True, default='How to write serializers?', description='question description')
})

answers = api.model('Answer Model', {
    'answer': fields.String(required=True, default='create a dictionary of data', description='answer description')
})
