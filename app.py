from flask import Flask, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy

from config import config

api = Blueprint('api', __name__)
db = SQLAlchemy()


@api.route('/')
def check_health():
    return jsonify({
        'success': True,
        'data': 'Healthy!',
    }), 200


@api.route('/movies')
def get_movies():
    movies = []
    return jsonify({
        'success': True,
        'movies': movies,
    }), 200


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    app.register_blueprint(api)
    return app
