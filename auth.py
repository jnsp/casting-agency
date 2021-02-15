from flask import request


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


class AuthError(Exception):
    pass
