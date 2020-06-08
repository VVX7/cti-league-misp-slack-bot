import requests

from flask import Flask
from flask import jsonify
from flask import request
from flask_slacksigauth import slack_sig_auth
from rq import Queue

from utils import run, build_response, valid_input
from config import DevelopmentConfig, ProductionConfig
from worker import conn

app = Flask(__name__)
app.config.from_object(ProductionConfig())

q = Queue(connection=conn)


@app.route('/')
def index():
    return 'MisInfoSec Tech'


@app.errorhandler(403)
def not_authorized(e):
    return jsonify(error=str(e)), 403


@slack_sig_auth
@app.route('/archive', methods=['POST'])
def archive():
    text=request.form['text']
    response_url=request.form['response_url']

    if valid_input(text):
        archive_url = text.split()[0]
        data = {
            'archive_url' : archive_url,
            'response_url': response_url
        }
        q.enqueue(run, data)
        resp = build_response('Archiving {}.'.format(archive_url))
        requests.post(response_url, json=resp)
    else:
        resp = build_response('Unable to archive: {}'.format(text))
        requests.post(response_url, json=resp)

    return ('', 200)

