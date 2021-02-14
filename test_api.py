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


def test_get_movies(client):
    db.session.add(Movie(title='TITLE', release_date=date(2020, 1, 1)))
    db.session.commit()

    res = client.get('/movies')
    expected = {
        'success': True,
        'movies': [{
            'title': 'TITLE',
            'release_date': '2020-01-01'
        }],
    }
    assert res.get_json() == expected


def test_make_movie(client):
    res = client.post('/movies',
                      json={
                          'title': 'NEW_MOVIE',
                          'release_date': '2020-01-02'
                      })
    expected = {
        'success': True,
        'movies': [{
            'title': 'NEW_MOVIE',
            'release_date': '2020-01-02'
        }]
    }
    assert res.get_json() == expected


def test_movie_wrong_date_format(client):
    res = client.post('/movies',
                      json={
                          'title': 'NEW_MOVIE',
                          'release_date': '020-01-02'
                      })
    assert res.status_code == 400
