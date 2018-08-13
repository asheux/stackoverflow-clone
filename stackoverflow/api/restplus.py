import logging
from flask import Blueprint
from flask_restplus import Api

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
log = logging.getLogger(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, authorizations=authorizations, version='1.0', title='Stackoverflow-lite API',
          description=(
            "This is an api for StackOverflow-lite platform where people can ask questions and provide answers.\n\n"
            "##Exploring the demo.\n"
            "Create a new user at the 'POST /auth/register' endpoint. Get the user access token from the response."
            "Click the authorize button and add the token in the following format.\n\n"
            "`Bearer (jwt-token without the brackets)`\n\n"

            "## Authorization token (using)\n"
            "`Jwt-Extended`"
        ),
    )
