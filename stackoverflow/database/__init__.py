from flask_jwt_extended import get_jwt_identity, jwt_required

db = {}
blacklistdb = {}

@jwt_required
def get_current_user():
    from stackoverflow.api.v1.auth.collections import store
    return store.get_by_field(key='username', value=get_jwt_identity())
