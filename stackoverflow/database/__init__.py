"""
Imports

"""
from flask_jwt_extended import get_jwt_identity, jwt_required

db = {}
blacklistdb = {}
questionsdb = {}
answersdb = {}

@jwt_required
def get_current_user():
    """get the currently logged in user"""
    from stackoverflow.api.v1.auth.collections import store
    return store.get_by_field(key='username', value=get_jwt_identity())
