from flask import Blueprint, jsonify

from models import Movie

api = Blueprint('api', __name__)


@api.route('/')
def check_health():
    return jsonify({
        'success': True,
        'data': 'Healthy!',
    }), 200


@api.route('/movies')
def get_movies():
    movies = [m.to_dict() for m in Movie.query.all()]
    return jsonify({
        'success': True,
        'movies': movies,
    }), 200
