import os

from flask import Flask, jsonify

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# TODO: Make create_app
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def check_health():
    return jsonify({
        'success': True,
        'data': 'Healthy!',
    }), 200


@app.route('/movies')
def get_movies():
    movies = []
    return jsonify({
        'success': True,
        'movies': movies,
    }), 200
