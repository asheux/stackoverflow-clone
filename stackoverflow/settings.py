import os

# Flask settings
FLASK_SERVER_NAME = '127.0.0.1:5000'
FLASK_DEBUG = True  # Do not use debug mode in production
TESTING = True
DEVELOPMENT = True

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = True
RESTPLUS_ERROR_404_HELP = False
RESTPLUS_MASK_HEADER = 'Authorization'

# aswer status
ACCEPT = True
PENDING = False
VOTES = 0
DOWNVOTE = VOTES - 1
DATABASE_URL = os.getenv('DATABASE_URL')

# Jwt settings
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_SECRET_KEY = os.urandom(24)
