from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    return app


app = create_app('default')


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
