from datetime import date

import pytest

from app import create_app, db
from models import Movie


@pytest.fixture
def client():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_health(client):
    res = client.get('/')
    expected = {
        'success': True,
        'data': 'Healthy!',
    }
    assert res.get_json() == expected


def test_get_movies(client):
    db.session.add(Movie(title='TITLE', release_date=date(2020, 1, 1)))
    db.session.commit()

    res = client.get('/movies')
    expected = {
        'success':
        True,
        'movies': [{
            'title': 'TITLE',
            'release_date': 'Wed, 01 Jan 2020 00:00:00 GMT'
        }],
    }
    assert res.get_json() == expected
