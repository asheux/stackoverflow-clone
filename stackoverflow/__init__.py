import logging.config
import os
from urllib.parse import urlparse
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_restplus import Api
from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from stackoverflow import settings
from stackoverflow.base.routes import index_blueprint
from stackoverflow.api.restplus import blueprint, api, authorizations
from stackoverflow.api.v1.auth.routes.routes import ns as user_namespace
from stackoverflow.api.v1.questions.routes import ns as question_namespace

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

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
    def __init__(self, conf):
        self.config = database_config(conf)

    def init_db(self):
        self.connection = psycopg2.connect(**self.config)
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        self.connection.close()

v2_db = Database(settings.DATABASE_URL)
v2_blueprint = Blueprint('api_v2', __name__, url_prefix='/api/v2')
v2_api = Api(v2_blueprint, authorizations=authorizations, version='1.1', title='V2 of stackoverflow-lite questions API',
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

def configure_app(flask_app):
    from stackoverflow.api.v2.auth.routes.routes import ns as v2_user_namespace
    from stackoverflow.api.v2.questions.routes import ns as q_namespace
    from stackoverflow.api.v2.questions.answer_routes import ns as q_namespace
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
    configure_app(flask_app)
    jwt = JWTManager(flask_app)

    jwt._set_error_handler_callbacks(api)
    jwt._set_error_handler_callbacks(v2_api)
    flask_app.register_blueprint(index_blueprint)
    flask_app.register_blueprint(v2_blueprint)
    flask_app.register_blueprint(blueprint)
    v2_db.init_db()

    @jwt.token_in_blacklist_loader
    def check_token(token):
        from stackoverflow.api.v2.models import BlackList
        return BlackList.get_one_by_field(field='jti', value=token['jti']) is not None

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        from stackoverflow.api.v1.models import BlackListToken
        jti = decrypted_token['jti']
        return BlackListToken.check_blacklist(jti)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    initialize_app(app)

    log.info('Starting development server at http://{}'.format(settings.FLASK_SERVER_NAME))

    return app
