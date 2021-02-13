from flask import current_app
import pytest

from app import create_app, db


@pytest.fixture
def init_app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()


def test_app_exists(init_app):
    assert current_app is not None


def test_app_is_testing(init_app):
    assert current_app.config['TESTING'] is True
