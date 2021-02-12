from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def check_health():
    return jsonify({
        'success': True,
        'data': 'Healthy!',
    }), 200


@app.route('/movies')
def get_movies():
    movies = [1, 2, 3]
    return jsonify({
        'success': True,
        'movies': movies,
    }), 200
