from flask_restplus import fields
from stackoverflow.api.restplus import api

register_data = dict(
    name=fields.String(required=True, default='Paulla Mboya', description='User fullname'),
    username=fields.String(required=True, default='paulla', description='Username'),
    email=fields.String(required=True, default='paulla@gmail.com', description='The user\'s email address'),
    password=fields.String(required=True, default='barryazah', description='The users secret password'),
)
user_register = api.model('Register Model', register_data)

head = 'Flask restful app'
desc = 'How to build a restful api in flask'
questions_data = dict(
    title=fields.String(required=True, default=head, description='Question name'),
    description=fields.String(required=True, default=desc, description='the question description here')
)
questions = api.model('Question Model', questions_data)

answers = api.model('Answer Model', {
    'answer': fields.String(required=True, default='create a dictionary of data', description='answer description')
})
