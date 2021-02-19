from datetime import date

import pytest

from app import create_app, db
from app.models import Movie, Actor, ValidationError


@pytest.fixture(autouse=True)
def init_test_db():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()


def test_movie_model():
    first_movie = Movie(title='TITLE1', release_date=date(2020, 1, 1))
    first_movie.save()
    second_movie = Movie(title='TITLE2', release_date=date(2020, 1, 2))
    second_movie.save()

    saved_movies = Movie.query.all()
    assert len(saved_movies) == 2

    first_saved_movie = Movie.query.get(1)
    assert first_saved_movie.title == 'TITLE1'
    assert first_saved_movie.release_date == date(2020, 1, 1)

    second_saved_movie = Movie.query.get(2)
    assert second_saved_movie.title == 'TITLE2'
    assert second_saved_movie.release_date == date(2020, 1, 2)

    first_saved_movie.remove()
    assert Movie.query.get(1) is None


def test_movie_to_dict():
    movie = Movie(title='TITLE', release_date=date(2020, 1, 1))
    assert movie.to_dict() == {
        'id': None,
        'title': 'TITLE',
        'release_date': '2020-01-01',
    }


def test_actor_model():
    first_actor = Actor(name='ACTOR1', age=10, gender='F')
    first_actor.save()
    second_actor = Actor(name='ACTOR2', age=20, gender='M')
    second_actor.save()

    saved_actors = Actor.query.all()
    assert len(saved_actors) == 2

    first_saved_actor = Actor.query.get(1)
    assert first_saved_actor.name == 'ACTOR1'
    assert first_saved_actor.age == 10
    assert first_saved_actor.gender == 'F'

    second_saved_actor = Actor.query.get(2)
    assert second_saved_actor.name == 'ACTOR2'
    assert second_saved_actor.age == 20
    assert second_saved_actor.gender == 'M'

    first_saved_actor.remove()
    assert Actor.query.get(1) is None


def test_actor_non_negative_age():
    with pytest.raises(ValidationError, match='Age is negative'):
        Actor(age=-1)


def test_actor_to_dict():
    actor = Actor(name='Actor', age=10, gender='F')
    assert actor.to_dict() == {
        'id': None,
        'name': 'Actor',
        'age': 10,
        'gender': 'F'
    }
