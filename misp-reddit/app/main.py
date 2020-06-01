import requests

from flask import Flask
from flask import jsonify
from flask import request
from flask_slacksigauth import slack_sig_auth
from rq import Queue

from utils import process_reddit_account, process_reddit_comment, process_reddit_post, process_reddit_subreddit
from utils import build_response, valid_reddit_account
from config import DevelopmentConfig, ProductionConfig
from worker import conn

app = Flask(__name__)
app.config.from_object(ProductionConfig())

q = Queue(connection=conn)


@app.route('/', methods=['GET', 'POST'])
def index():
    j=request.json
    print(j)
    return('', 200)


@app.errorhandler(403)
def not_authorized(e):
    return jsonify(error=str(e)), 403


@app.route('/reddit_account', methods=['POST'])
@slack_sig_auth
def reddit_account():
    text=request.form['text']
    response_url=request.form['response_url']

    if valid_reddit_account(text):
        misp_event_id = text.split(" ")[0]
        reddit_account = text.split(" ")[1]
        data = {
            'misp_event_id' : misp_event_id,
            'reddit_account' : reddit_account,
            'response_url': response_url
        }
        q.enqueue(process_reddit_account, data)
        resp = build_response('Adding Reddit account {} to MISP Event {}.'.format(reddit_account, misp_event_id))
        requests.post(response_url, json=resp)
    else:
        resp = build_response('Invalid Reddit account or MISP Event: {}'.format(text))
        requests.post(response_url, json=resp)

    return ('', 200)

@app.route('/reddit_subreddit', methods=['POST'])
@slack_sig_auth
def subreddit():
    text = request.form['text']
    response_url = request.form['response_url']

    misp_event_id = text.split(' ')[0]
    reddit_subreddit = text.split(' ')[1]

    data = {
        'misp_event_id' : misp_event_id,
        'reddit_subreddit' : reddit_subreddit,
        'response_url' : response_url
    }

    q.enqueue(process_reddit_subreddit, data)
    resp = build_response(f'Adding Reddit subreddit {reddit_subreddit} to MISP Event {misp_event_id}')
    requests.post(response_url, json=resp)

    return('', 200)


@app.route('/reddit_post', methods=['POST'])
@slack_sig_auth
def reddit_post():
    text = request.form['text']
    response_url = request.form['response_url']

    misp_event_id = text.split(' ')[0]
    reddit_post_id = text.split(' ')[1]

    data = {
        'misp_event_id' : misp_event_id,
        'reddit_post_id' : reddit_post_id,
        'response_url' : response_url
    }

    q.enqueue(process_reddit_post, data)
    resp = build_response(f'Adding Reddit post {reddit_post_id} to MISP Event {misp_event_id}')
    requests.post(response_url, json=resp)

    return('', 200)

@app.route('/reddit_comment', methods=['POST'])
@slack_sig_auth
def reddit_comment():
    text = request.form['text']
    response_url = request.form['response_url']

    misp_event_id = text.split(' ')[0]
    reddit_comment = text.split(' ')[1]

    data = {
        'misp_event_id' : misp_event_id,
        'reddit_comment_id' : reddit_comment,
        'response_url' : response_url
    }

    q.enqueue(process_reddit_comment, data)
    resp = build_response(f'Adding Reddit comment {reddit_comment} to MISP Event {misp_event_id}')
    requests.post(response_url, json=resp)

    return('', 200)


#
# if __name__ == "__main__":
#     app.run("0.0.0.0")
