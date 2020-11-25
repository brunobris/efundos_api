from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims or claims['roles'] != 'admin':
            return jsonify(msg='Admins only!'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper

# Decorator para permitir acesso apenas ao scraper
def scraper_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims or claims['roles'] != 'scraper':
            return jsonify(msg='Este endpoint não pode ser chamado por usuários'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper
