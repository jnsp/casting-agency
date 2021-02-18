from datetime import date

import pytest

from api import convert_str_to_date
from app import create_app, db
from fake_jwt import get_fake_token
from models import Movie, Actor


@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        app.config['USE_FAKE_JWKS'] = True
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


class TestMovie:
    @pytest.fixture
    def test_movie(self):
        movie = Movie(title='MOVIE', release_date=date(2021, 1, 1))
        movie.save()
        return movie

    @pytest.fixture
    def new_movie_info(self):
        return {'title': 'NEW_MOVIE', 'release_date': '2021-02-01'}

    def header(self, permission):
        token = get_fake_token([permission])
        return {'Authorization': f'bearer {token}'}

    def test_get_movies(self, client, test_movie):
        res = client.get('/movies', headers=self.header('view:movies'))

        expected = {'success': True, 'movies': [test_movie.to_dict()]}
        assert res.get_json() == expected

    def test_get_empty_movies_when_no_data(self, client):
        res = client.get('/movies', headers=self.header('view:movies'))

        expected = {'success': True, 'movies': []}
        assert res.get_json() == expected

    def test_make_movie(self, client, new_movie_info):
        res = client.post('/movies',
                          json=new_movie_info,
                          headers=self.header('add:movies'))
        expected = {'success': True, 'movie': new_movie_info}
        assert res.get_json() == expected

        movie = Movie.query.get(1)
        assert movie.to_dict() == new_movie_info

    def test_date_format(self, client, new_movie_info):
        new_movie_info['release_date'] = 'Tue Aug 16 1988'
        res = client.post('/movies',
                          json=new_movie_info,
                          headers=self.header('add:movies'))
        assert res.status_code == 400
        assert res.get_json() == {
            'success': False,
            'error': 'Wrong date format: YYYY-MM-DD',
        }

    def test_modify_movie(self, client, test_movie, new_movie_info):
        res = client.patch('/movies/1',
                           json=new_movie_info,
                           headers=self.header('modify:movies'))
        expected = {'success': True, 'movie': new_movie_info}
        assert res.get_json() == expected

        movie = Movie.query.get(1)
        assert movie.to_dict() == new_movie_info

    def test_not_found_error_when_modify(self, client):
        res = client.patch('/movies/1', headers=self.header('modify:movies'))
        assert res.status_code == 404
        assert res.get_json({'success': False, 'error': 'Not found'})

    def test_remove_movie(self, client, test_movie):
        res = client.delete('/movies/1', headers=self.header('delete:movies'))
        expected = {'success': True, 'deleted': test_movie.to_dict()}

        assert res.get_json() == expected
        assert Movie.query.get(1) is None

    def test_not_found_error_when_remove(self, client):
        res = client.delete('/movies/1', headers=self.header('delete:movies'))
        assert res.status_code == 404
        assert res.get_json({'success': False, 'error': 'Not found'})


@pytest.fixture
def test_actor():
    actor = Actor(name='ACTOR', age=10, gender='F')
    actor.save()
    return actor


@pytest.fixture
def new_actor_info():
    return {'name': 'NEW_ACTOR', 'age': 20, 'gender': 'X'}


class TestActor:
    @pytest.fixture
    def test_actor(self):
        actor = Actor(name='ACTOR', age=10, gender='F')
        actor.save()
        return actor

    @pytest.fixture
    def new_actor_info(self):
        return {'name': 'NEW_ACTOR', 'age': 20, 'gender': 'X'}

    def test_get_actors(self, client, test_actor):
        res = client.get('/actors')
        expected = {'success': True, 'actors': [test_actor.to_dict()]}
        assert res.get_json() == expected

    def test_make_actor(self, client, new_actor_info):
        res = client.post('/actors', json=new_actor_info)
        expected = {'success': True, 'actor': new_actor_info}
        assert res.get_json() == expected

        actor = Actor.query.get(1)
        assert actor.to_dict() == new_actor_info

    def test_modify_actor(self, client, test_actor, new_actor_info):
        res = client.patch('/actors/1', json=new_actor_info)
        expected = {'success': True, 'actor': new_actor_info}
        assert res.get_json() == expected

        actor = Actor.query.get(1)
        assert actor.to_dict() == new_actor_info

    def test_not_found_error_when_modify(self, client):
        res = client.patch('/actors/1')
        assert res.status_code == 404
        assert res.get_json({'success': False, 'error': 'Not found'})

    def test_remove_actor(self, client, test_actor):
        res = client.delete('/actors/1')
        expected = {'success': True, 'deleted': test_actor.to_dict()}
        assert res.get_json() == expected
        assert Actor.query.get(1) is None

    def test_not_found_error_when_remove(self, client):
        res = client.delete('/actors/1')
        assert res.status_code == 404
        assert res.get_json({'success': False, 'error': 'Not found'})


def test_convert_str_to_date():
    assert convert_str_to_date('2021-01-01') == date(2021, 1, 1)
