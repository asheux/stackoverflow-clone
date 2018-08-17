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
DATABASE_URL = 'postgres://pjvmdmcqfvaqgw:827f38aa834a1513d332505d119a804d06977472ba52797717628a98c05daf1c@ec2-54-235-242-63.compute-1.amazonaws.com:5432/dbdp9cg15rds46'

# Jwt settings
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_SECRET_KEY = 'this aint your mama'
