import base64
import json

from dotenv import dotenv_values
import pytest
import requests

from app import create_app
from auth import get_auth_token, validate_jwt, AuthError


@pytest.fixture()
def app():
    return create_app('testing')


def test_get_auth_token(app):
    token_header = {'Authorization': 'bearer TOKEN'}

    with app.test_request_context(headers=token_header):
        assert get_auth_token() == 'TOKEN'


def test_autherror_without_auth_header(app):
    no_header = {}

    with app.test_request_context(headers=no_header):
        with pytest.raises(AuthError, match='No Authorization header'):
            get_auth_token()


def test_autherror_when_auth_splited_improperly(app):
    too_many_splited_header = {'Authorization': 'A B C'}

    with app.test_request_context(headers=too_many_splited_header):
        with pytest.raises(AuthError, match='Token splited too few or many'):
            get_auth_token()


def test_autherror_when_auth_type_is_not_bearer(app):
    not_bearer_token_header = {'Authorization': 'basic TOKEN'}

    with app.test_request_context(headers=not_bearer_token_header):
        with pytest.raises(AuthError, match='Not bearer auth type'):
            get_auth_token()


def test_validate_jwt():
    test_token = get_test_jwt()
    expected_payload = json.loads(
        base64.b64decode(test_token.split('.')[1]).decode('utf-8'))
    assert validate_jwt(test_token) == expected_payload


def test_autherror_when_token_has_no_kid():
    test_header = base64.b64encode(
        b'{"no_kid": "aVcItGAydwX7JUBqWl1Qq"}').decode('utf-8')
    no_kid_token = test_header + '..'

    with pytest.raises(AuthError, match="Token has no kid"):
        validate_jwt(no_kid_token)


def get_test_jwt():
    config = {**dotenv_values('.env.shared'), **dotenv_values('.env.secret')}

    url = f"https://{config['AUTH0_DOMAIN']}/oauth/token"
    headers = {'content-type': 'application/json'}
    data = {
        'client_id': config['TEST_CLIENT_ID'],
        'client_secret': config['TEST_CLIENT_SECRET'],
        'audience': config['API_AUDIENCE'],
        'grant_type': 'client_credentials',
    }
    res = requests.post(url, headers=headers, json=data)

    return res.json()['access_token']
