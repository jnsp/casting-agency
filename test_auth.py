import pytest

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
