from datetime import datetime
import os

from dotenv import load_dotenv
from flask import Blueprint, jsonify, request, abort, redirect

from .auth import require_auth, AuthError
from .models import Movie, Actor

api = Blueprint('api', __name__)
load_dotenv()


@api.route('/login')
def login():
    auth0_login_url = (f'https://{os.getenv("AUTH0_DOMAIN")}/authorize?'
                       f'audience={os.getenv("API_AUDIENCE")}&'
                       'response_type=token&'
                       f'client_id={os.getenv("CLIENT_ID")}&'
                       f'redirect_uri={os.getenv("APP_URL")}/callback&'
                       'state=STATE')
    return redirect(auth0_login_url, 302)


@api.route('/callback')
def callback():
    return 'Logged-in!'


@api.route('/movies')
@require_auth(permission='view:movies')
def get_movies():
    movies = [m.to_dict() for m in Movie.query.all()]
    return jsonify({
        'success': True,
        'movies': movies,
    }), 200


@api.route('/movies', methods=['POST'])
@require_auth(permission='add:movies')
def make_movie():
    body = request.get_json()
    try:
        movie = Movie(title=body['title'],
                      release_date=convert_str_to_date(body['release_date']))
    except ValueError:
        abort(400, 'Wrong date format: YYYY-MM-DD')
    else:
        movie.save()

    return jsonify({
        'success': True,
        'movie': movie.to_dict(),
    }), 200


@api.route('/movies/<int:id>', methods=['PATCH'])
@require_auth(permission='modify:movies')
def modify_movie(id):
    body = request.get_json()
    movie = Movie.query.get_or_404(id)

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


@api.route('/movies/<int:id>', methods=['DELETE'])
@require_auth(permission='delete:movies')
def remove_movie(id):
    movie = Movie.query.get_or_404(id)
    movie.remove()
    return jsonify({
        'success': True,
        'deleted': movie.to_dict(),
    })


@api.route('/actors')
@require_auth(permission='view:actors')
def get_actors():
    actors = [a.to_dict() for a in Actor.query.all()]
    return jsonify({
        'success': True,
        'actors': actors,
    }), 200


@api.route('/actors', methods=['POST'])
@require_auth(permission='add:actors')
def make_actor():
    body = request.get_json()
    actor = Actor(**body)
    actor.save()

    return jsonify({'success': True, 'actor': actor.to_dict()})


@api.route('/actors/<int:id>', methods=['PATCH'])
@require_auth(permission='modify:actors')
def modify_actor(id):
    body = request.get_json()
    actor = Actor.query.get_or_404(id)

    if (name := body.get('name')):
        actor.name = name
    if (age := body.get('age')):
        actor.age = age
    if (gender := body.get('gender')):
        actor.gender = gender

    actor.save()

    return jsonify({
        'success': True,
        'actor': actor.to_dict(),
    })


@api.route('/actors/<int:id>', methods=['DELETE'])
@require_auth(permission='delete:actors')
def remove_actor(id):
    actor = Actor.query.get_or_404(id)
    actor.remove()

    return jsonify({
        'success': True,
        'deleted': actor.to_dict(),
    })


@api.app_errorhandler(400)
def bad_request(e):
    return jsonify({
        'success': False,
        'error': e.description,
    }), 400


@api.app_errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Not found',
    }), 404


@api.app_errorhandler(405)
def methoed_not_allowed(e):
    return jsonify({
        'success': False,
        'error': 'Method now allowed',
    })


@api.app_errorhandler(AuthError)
def forbidden(e):
    return jsonify({
        'success': False,
        'error': e.error,
    }), e.status_code


def convert_str_to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()
