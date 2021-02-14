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
                      release_date=datetime.strptime(body['release_date'],
                                                     '%Y-%m-%d').date())
    except ValueError:
        abort(400)
    else:
        movie.save()

    movies = [m.to_dict() for m in Movie.query.all()]
    return jsonify({
        'success': True,
        'movies': movies,
    }), 200


@api.route('/actors')
def get_actors():
    actors = [a.to_dict() for a in Actor.query.all()]
    return jsonify({
        'success': True,
        'actors': actors,
    }), 200
