from flask import Flask


app = Flask(__name__)


@app.route('/')
def check_health():
    return 'healthy'
