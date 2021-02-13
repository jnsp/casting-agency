from datetime import date

import pytest

from app import app
from models import db, Movie, Actor, ValidationError


@pytest.fixture
def init_test_db():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()


def test_movie_model(init_test_db):
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


def test_actor_model(init_test_db):
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


def test_actor_non_negative_age(init_test_db):
    with pytest.raises(ValidationError, match='Age is negative'):
        Actor(age=-1)
