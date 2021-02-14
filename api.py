from datetime import datetime
from flask import Blueprint, jsonify, request, abort

from models import Movie, Actor

api = Blueprint('api', __name__)


@api.route('/movies')
def get_movies():
    movies = [m.to_dict() for m in Movie.query.all()]
    return jsonify({
        'success': True,
        'movies': movies,
    }), 200


@api.route('/movies', methods=['POST'])
def make_movie():
    body = request.get_json()
    try:
        movie = Movie(title=body['title'],
                      release_date=convert_str_to_date(body['release_date']))
    except ValueError:
        abort(400)
    else:
        movie.save()

    return jsonify({
        'success': True,
        'movie': movie.to_dict(),
    }), 200


@api.route('/movies/<int:id>', methods=['PATCH'])
def modify_movie(id):
    body = request.get_json()
    movie = Movie.query.get(id)

    if (title := body.get('title')):
        movie.title = title
    if (release_date := body.get('release_date')):
        release_date = convert_str_to_date(release_date)
        movie.release_date = release_date

    movie.save()

    return jsonify({
        'success': True,
        'movie': movie.to_dict(),
    })


@api.route('/actors')
def get_actors():
    actors = [a.to_dict() for a in Actor.query.all()]
    return jsonify({
        'success': True,
        'actors': actors,
    }), 200


@api.route('/actors', methods=['POST'])
def make_actor():
    body = request.get_json()
    actor = Actor(**body)
    actor.save()

    return jsonify({'success': True, 'actor': actor.to_dict()})


def convert_str_to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()
