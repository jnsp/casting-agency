from functools import wraps

from dotenv import dotenv_values
from flask import request, current_app
from jose import jwt
import requests

import fake_jwt

config = {**dotenv_values('.env.shared'), **dotenv_values('.env.secret')}


def get_auth_token():
    if (auth_header := request.headers.get('Authorization')) is None:
        raise AuthError('No Authorization header', 401)

    auth_parts = auth_header.split(' ')
    if len(auth_parts) != 2:
        raise AuthError('Token splited too few or many', 401)

    auth_type, token = auth_parts
    if auth_type.lower() != 'bearer':
        raise AuthError('Not bearer auth type', 401)

    return token


def get_jwks():
    jwks_url = f"https://{config['AUTH0_DOMAIN']}/.well-known/jwks.json"
    return requests.get(jwks_url).json()


def validate_jwt(token, jwks):
    try:
        token_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError('Unable decoding token headers', 401)

    if not (kid := token_header.get('kid')):
        raise AuthError('Token has no kid', 401)

    if not (signing_key := [k for k in jwks['keys'] if k['kid'] == kid]):
        raise AuthError('No matched kid', 401)

    try:
        payload = jwt.decode(token,
                             signing_key[0],
                             algorithms=config['ALGORITHM'],
                             audience=config['API_AUDIENCE'],
                             issuer=f"https://{config['AUTH0_DOMAIN']}/")
    except jwt.ExpiredSignatureError:
        raise AuthError('Token is expired', 401)
    except jwt.JWTClaimsError:
        raise AuthError('Invalid claim', 401)
    except Exception:
        raise AuthError('Unable validate token', 401)

    return payload


def check_permission(permission, payload):
    if (permissions := payload.get('permissions')) is None:
        raise AuthError('Payload has NO permissions', 403)

    if permission and permission not in permissions:
        raise AuthError('Permission not found', 403)

    return True


def require_auth(permission=None):
    def _require_auth(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_auth_token()
            use_test_jwks = current_app.config.get('USE_FAKE_JWKS')
            jwks = get_jwks() if not use_test_jwks else fake_jwt.jwks
            payload = validate_jwt(jwt, jwks)
            check_permission(permission, payload)
            return f(*args, **kwargs)

        return wrapper

    return _require_auth


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
