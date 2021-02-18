import json
from base64 import b64encode, b64decode

from dotenv import dotenv_values
import pytest
import requests

from app import create_app
from app.auth import get_auth_token, get_jwks, validate_jwt, \
    check_permission, AuthError


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
            with pytest.raises(AuthError) as e:
                get_auth_token()
            assert e.value.error == 'No Authorization header'
            assert e.value.status_code == 401

    def test_autherror_when_auth_splited_improperly(self, app):
        too_many_splited_header = {'Authorization': 'A B C'}

        with app.test_request_context(headers=too_many_splited_header):
            with pytest.raises(AuthError) as e:
                get_auth_token()
            assert e.value.error == 'Token splited too few or many'
            assert e.status_code == 401

    def test_autherror_when_auth_type_is_not_bearer(self, app):
        not_bearer_token_header = {'Authorization': 'basic TOKEN'}

        with app.test_request_context(headers=not_bearer_token_header):
            with pytest.raises(AuthError) as e:
                get_auth_token()
            assert e.value.error == 'Not bearer auth type'
            assert e.status_code == 401


class TestValidateJWT:
    @pytest.fixture(scope='class')
    def jwks(self):
        return get_jwks()

    def test_validate_jwt(self, jwks):
        test_token = self.get_test_jwt()
        expected_payload = json.loads(
            b64decode(test_token.split('.')[1]).decode('utf-8'))
        assert validate_jwt(test_token, jwks) == expected_payload

    def test_autherror_when_token_has_no_header(self, jwks):
        no_header_token = 'TOKEN'

        with pytest.raises(AuthError) as e:
            validate_jwt(no_header_token, jwks)
        assert e.value.error == 'Unable decoding token headers'
        assert e.value.status_code == 401

    def test_autherror_when_token_has_no_kid(self, jwks):
        no_kid_header = b64encode(b'{"no_kid": "KID"}').decode('utf-8')
        no_kid_token = no_kid_header + '..'

        with pytest.raises(AuthError) as e:
            validate_jwt(no_kid_token, jwks)
        assert e.value.error == 'Token has no kid'
        assert e.value.status_code == 401

    def test_autherror_when_no_matched_kid(self, jwks):
        unmatched_header = b64encode(b'{"kid": "KID"}').decode('utf-8')
        unmatched_token = unmatched_header + '..'

        with pytest.raises(AuthError) as e:
            validate_jwt(unmatched_token, jwks)
        assert e.value.error == 'No matched kid'
        assert e.value.status_code == 401

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

        with pytest.raises(AuthError) as e:
            check_permission(permission, not_permitted_payload)
        assert e.value.error == 'Permission not found'
        assert e.value.status_code == 403

    def test_autherror_when_payload_has_no_permissions(self):
        any_permission = 'any permission'
        no_permissions_payload = {'no_permissions': ['any permissions']}

        with pytest.raises(AuthError) as e:
            check_permission(any_permission, no_permissions_payload)
        assert e.value.error == 'Payload has NO permissions'
        assert e.value.status_code == 403
