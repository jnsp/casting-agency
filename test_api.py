from datetime import date

import pytest

from app import create_app, db
from models import Movie, Actor


@pytest.fixture
def client():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


class MovieTest:
    def test_get_movies(self, client):
        Movie(title='TITLE', release_date=date(2020, 1, 1)).save()

        res = client.get('/movies')
        expected = {
            'success': True,
            'movies': [{
                'title': 'TITLE',
                'release_date': '2020-01-01'
            }],
        }
        assert res.get_json() == expected

    def test_make_movie(self, client):
        res = client.post('/movies',
                          json={
                              'title': 'NEW_MOVIE',
                              'release_date': '2020-01-02'
                          })
        expected = {
            'success': True,
            'movie': {
                'title': 'NEW_MOVIE',
                'release_date': '2020-01-02'
            }
        }
        assert res.get_json() == expected

        movie = Movie.query.get(1)
        assert movie.to_dict() == {
            'title': 'NEW_MOVIE',
            'release_date': '2020-01-02'
        }

    def test_movie_wrong_date_format(self, client):
        res = client.post('/movies',
                          json={
                              'title': 'NEW_MOVIE',
                              'release_date': '020-01-02'
                          })
        assert res.status_code == 400


class ActorTest:
    def test_get_actors(self, client):
        Actor(name='ACTOR', age=10, gender='F').save()

        res = client.get('/actors')
        expected = {
            'success': True,
            'actors': [{
                'name': 'ACTOR',
                'age': 10,
                'gender': 'F',
            }]
        }
        assert res.get_json() == expected

    def test_make_actor(self, client):
        res = client.post('/actors',
                          json={
                              'name': 'NEW_ACTOR',
                              'age': 20,
                              'gender': 'M'
                          })
        expected = {
            'success': True,
            'actor': {
                'name': 'NEW_ACTOR',
                'age': 20,
                'gender': 'M'
            }
        }
        assert res.get_json() == expected

        actor = Actor.query.get(1)
        assert actor.to_dict() == {
            'name': 'NEW_ACTOR',
            'age': 20,
            'gender': 'M'
        }
