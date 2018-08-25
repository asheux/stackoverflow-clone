"""
Imports

"""
import os
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_restplus import Api
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from stackoverflow import settings
from stackoverflow.base.routes import index_blueprint
from stackoverflow.api.restplus import BLUEPRINT, API, AUTHORIZATIONS
from stackoverflow.api.v1.auth.routes.routes import NS as user_namespace
from stackoverflow.api.v1.questions.routes import NS as question_namespace


def database_config(db_url):
    """This creates the database configuration"""
    url = urlparse(db_url)

    if os.environ.get('DATABASE_URL'):
        database_uri = os.environ.get('DATABASE_URL')

    config = dict(
        dbname=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return config


class Database:
    """Connecting to the database"""
    def __init__(self, conf):
        self.config = database_config(conf)

    def init_db(self):
        """Initializes the database"""
        self.connection = psycopg2.connect(**self.config)
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        self.connection.close()

V2_DB = Database(settings.DATABASE_URL)
V2_BLUEPRINT = Blueprint('api_v2', __name__, url_prefix='/api/v2')
V2_API = Api(V2_BLUEPRINT, authorizations=AUTHORIZATIONS, version='1.1',
             title='V2 of stackoverflow-lite questions API',
             description=(
                 "This is an api for StackOverflow-lite platform \
                 where people can ask questions and provide answers.\n\n"
                 "##Exploring the demo.\n"
                 "Create a new user at the 'POST /auth/register' endpoint. \
                 Get the user access token from the response."
                 "Click the authorize button and add the token in the following format.\n\n"
                 "`Bearer (jwt-token without the brackets)`\n\n"

                 "## Authorization token (using)\n"
                 "`Jwt-Extended`"
             ),
             )

def configure_app(flask_app):
    """Configures the app"""
    from stackoverflow.api.v2.auth.routes.routes import NS as v2_user_namespace
    from stackoverflow.api.v2.questions.routes import NS as q_namespace
    from stackoverflow.api.v2.questions.answer_routes import NS as q_namespace
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    flask_app.config['JWT_BLACKLIST_ENABLED'] = settings.JWT_BLACKLIST_ENABLED
    flask_app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = settings.JWT_BLACKLIST_TOKEN_CHECKS
    flask_app.config['TESTING'] = settings.TESTING
    flask_app.config['DATABASE_URL'] = settings.DATABASE_URL

def initialize_app(flask_app):
    """Runs the configuration"""
    configure_app(flask_app)
    CORS(flask_app)
    jwt = JWTManager(flask_app)

    jwt._set_error_handler_callbacks(API)
    jwt._set_error_handler_callbacks(V2_API)
    flask_app.register_blueprint(index_blueprint)
    flask_app.register_blueprint(V2_BLUEPRINT)
    flask_app.register_blueprint(BLUEPRINT)
    V2_DB.init_db()

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        """Checks for blacklisted tokens"""
        from stackoverflow.api.v1.models import BlackListToken
        jti = decrypted_token['jti']
        return BlackListToken.check_blacklist(jti)

    @jwt.token_in_blacklist_loader
    def check_token(token):
        """Checks if token has been blacklisted"""
        from stackoverflow.api.v2.models import BlackList
        return BlackList.get_one_by_field(field='jti', value=token['jti']) is not None

def create_app(config_name):
    """Creates the flask app"""
    app = Flask(__name__)
    app.config.from_object(config_name)
    initialize_app(app)

    return app
