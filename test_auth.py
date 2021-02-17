import json
from base64 import b64encode, b64decode

from dotenv import dotenv_values
import pytest
import requests

from app import create_app
from auth import get_auth_token, validate_jwt, check_permission, AuthError


class TESTAuthToken:
    @pytest.fixture()
    def app(self):
        return create_app('testing')

    def test_get_auth_token(self, app):
        token_header = {'Authorization': 'bearer TOKEN'}

        with app.test_request_context(headers=token_header):
            assert get_auth_token() == 'TOKEN'

    def test_autherror_without_auth_header(self, app):
        no_header = {}

        with app.test_request_context(headers=no_header):
            with pytest.raises(AuthError, match='No Authorization header'):
                get_auth_token()

    def test_autherror_when_auth_splited_improperly(self, app):
        too_many_splited_header = {'Authorization': 'A B C'}

        with app.test_request_context(headers=too_many_splited_header):
            with pytest.raises(AuthError,
                               match='Token splited too few or many'):
                get_auth_token()

    def test_autherror_when_auth_type_is_not_bearer(self, app):
        not_bearer_token_header = {'Authorization': 'basic TOKEN'}

        with app.test_request_context(headers=not_bearer_token_header):
            with pytest.raises(AuthError, match='Not bearer auth type'):
                get_auth_token()


class TestValidateJWT:
    def test_validate_jwt(self):
        test_token = self.get_test_jwt()
        expected_payload = json.loads(
            b64decode(test_token.split('.')[1]).decode('utf-8'))
        assert validate_jwt(test_token) == expected_payload

    def test_autherror_when_token_has_no_header(self):
        no_header_token = 'TOKEN'

        with pytest.raises(AuthError, match='Unable decoding token headers'):
            validate_jwt(no_header_token)

    def test_autherror_when_token_has_no_kid(self):
        no_kid_header = b64encode(b'{"no_kid": "KID"}').decode('utf-8')
        no_kid_token = no_kid_header + '..'

        with pytest.raises(AuthError, match='Token has no kid'):
            validate_jwt(no_kid_token)

    def test_autherror_when_no_matched_kid(self):
        unmatched_header = b64encode(b'{"kid": "KID"}').decode('utf-8')
        unmatched_token = unmatched_header + '..'

        with pytest.raises(AuthError, match='No matched kid'):
            validate_jwt(unmatched_token)

    def get_test_jwt(self):
        config = {
            **dotenv_values('.env.shared'),
            **dotenv_values('.env.secret')
        }

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


class TestPermmision:
    def test_check_permission(self):
        permission = 'run:test'
        payload = {'permissions': ['run:test']}

        assert check_permission(permission, payload) is True

    def test_check_empty_permission(self):
        empty_permission = None
        payload = {'permissions': ['run:test']}

        assert check_permission(empty_permission, payload) is True

    def test_check_permission_not_permitted(self):
        permission = 'creat:test'
        not_permitted_payload = {'permissions': ['run:test']}

        with pytest.raises(AuthError, match='Permission not found'):
            check_permission(permission, not_permitted_payload)

    def test_autherror_when_payload_has_no_permissions(self):
        any_permission = 'any permission'
        no_permissions_payload = {'no_permissions': ['any permissions']}

        with pytest.raises(AuthError, match='Payload has NO permissions'):
            check_permission(any_permission, no_permissions_payload)
