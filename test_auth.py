import pytest

from app import create_app
from auth import get_auth_token, AuthError


@pytest.fixture()
def app():
    return create_app('testing')


def test_get_auth_token(app):
    with app.test_request_context(headers={'Authorization': 'bearer TOKEN'}):
        assert get_auth_token() == 'TOKEN'


def test_autherror_without_auth_header(app):
    with app.test_request_context():
        with pytest.raises(AuthError, match='No Authorization header'):
            get_auth_token()


def test_autherror_when_auth_splited_improperly(app):
    with app.test_request_context(headers={'Authorization': 'A B C'}):
        with pytest.raises(AuthError, match='Token splited too few or many'):
            get_auth_token()


def test_autherror_when_auth_type_is_not_bearer(app):
    with app.test_request_context(headers={'Authorization': 'basic TOKEN'}):
        with pytest.raises(AuthError, match='Not bearer auth type'):
            get_auth_token()
