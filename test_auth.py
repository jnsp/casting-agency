from dotenv import load_dotenv
import pytest
import requests
import os

from app import create_app
from auth import get_auth_token, AuthError


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


def get_test_jwt():
    load_dotenv()
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    TEST_CLIENT_ID = os.getenv('TEST_CLIENT_ID')
    TEST_CLIENT_SECRET = os.getenv('TEST_CLIENT_SECRET')
    API_AUDIENCE = os.getenv('API_AUDIENCE')

    url = f'https://{AUTH0_DOMAIN}/oauth/token'
    headers = {'content-type': 'application/json'}
    data = {
        'client_id': TEST_CLIENT_ID,
        'client_secret': TEST_CLIENT_SECRET,
        'audience': API_AUDIENCE,
        'grant_type': 'client_credentials',
    }
    res = requests.post(url, headers=headers, json=data)
    return res.json()['access_token']
