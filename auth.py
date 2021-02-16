from dotenv import dotenv_values
from flask import request
from jose import jwt
import requests


def get_auth_token():
    if (auth_header := request.headers.get('Authorization')) is None:
        raise AuthError('No Authorization header')

    auth_parts = auth_header.split(' ')
    if len(auth_parts) != 2:
        raise AuthError('Token splited too few or many')

    auth_type, token = auth_parts
    if auth_type.lower() != 'bearer':
        raise AuthError('Not bearer auth type')

    return token


def validate_jwt(token):
    config = {**dotenv_values('.env.shared'), **dotenv_values('.env.secret')}
    jwks_url = f"https://{config['AUTH0_DOMAIN']}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()

    if not (kid := jwt.get_unverified_header(token).get('kid')):
        raise AuthError('Token has no kid')

    if not (signing_key := [k for k in jwks['keys'] if k['kid'] == kid]):
        raise AuthError('No matched kid')

    payload = jwt.decode(token,
                         signing_key[0],
                         algorithms=config['ALGORITHM'],
                         audience=config['API_AUDIENCE'],
                         issuer=f"https://{config['AUTH0_DOMAIN']}/")
    return payload


class AuthError(Exception):
    pass
