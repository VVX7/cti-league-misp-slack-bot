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
@app.route('/misp_twitter', methods=['POST'])
def microblog():
    text=request.form['text']
    response_url=request.form['response_url']

    if valid_input(text):
        misp_event_id = text.split(" ")[0]
        twitter_post_id = text.split(" ")[1]
        data = {
            'misp_event_id' : misp_event_id,
            'twitter_post_id' : twitter_post_id,
            'response_url': response_url
        }
        q.enqueue(run, data)
        resp = build_response('Adding Twitter post {} to MISP Event {}.'.format(twitter_post_id, misp_event_id))
        requests.post(response_url, json=resp)
    else:
        resp = build_response('Invalid Twitter ID or MISP Event: {}'.format(text))
        requests.post(response_url, json=resp)

    return ('', 200)

#
# if __name__ == "__main__":
#     app.run("0.0.0.0")
