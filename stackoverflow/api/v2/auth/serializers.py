from flask_restplus import fields
from stackoverflow import v2_api

user_register = v2_api.model('Register Model', {
    'name': fields.String(required=True, default='Brian Mboya', description='User fullname'),
    'username': fields.String(required=True, default='asheuh', description='Username'),
    'email': fields.String(required=True, default='asheuh@gmail.com', description='The user\'s email address'),
    'password': fields.String(required=True, default='mermaid', description='The users secret password'),
})

data =  {
    'username': fields.String(required=True, default='asheuh', description='Your username'),
    'password': fields.String(required=True, default='mermaid', description='Your password'),
}
user_login = v2_api.model('Login Model', data)

questions = v2_api.model('Question Model', {
    'title': fields.String(required=True, default='Django restful api', description='Request name'),
    'description': fields.String(required=True, default='How to write serializers?', description='question description')
})

answers = v2_api.model('Answer Model', {
    'answer': fields.String(required=True, default='create a dictionary of data', description='answer description')
})
