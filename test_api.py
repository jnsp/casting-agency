from datetime import date

import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_health(client):
    res = client.get('/')
    expected = {
        'success': True,
        'data': 'Healthy!',
    }
    assert res.get_json() == expected


@pytest.mark.skip
def test_get_movies(client):
    res = client.get('/movies')
    expected = {
        'success': True,
        'movies': [{
            'title': 'TITLE',
            'release_date': date(2020, 2, 12)
        }],
    }
    assert res.get_json() == expected
