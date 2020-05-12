import requests

from flask import Flask
from flask import jsonify
from flask import request
from flask_slacksigauth import slack_sig_auth
from rq import Queue

from utils import run, build_response, valid_input
from config import ProductionConfig
from worker import conn

# Setup the flask app and load the config file.
# ProductionConfig should be used in production.
# Do not use Develop or Staging in prod as it exposes debug messages.
app = Flask(__name__)
app.config.from_object(ProductionConfig())

# This is the Redis queue.
# Tasks are added to the queue along with their URL callback to Slack.
q = Queue(connection=conn)


@app.route('/')
def index():
    """
    Returns default HTML page on app root.
    This function does not need to be modified when building a new bot app.
    :return:
    """
    return 'MisInfoSec Tech'


@app.errorhandler(403)
def not_authorized(e):
    """
    Handles unauthenticated requests.
    This function does not need to be modified when building a new bot app.
    :param e:
    :return:
    """
    return jsonify(error=str(e)), 403


@slack_sig_auth
@app.route('/misp_builtwith', methods=['POST'])
def tracking_id():
    """
    This is the endpoint that the Slack app POSTs to.
    Change the function route ('/misp_builtwith') to something unique for your bot.
    :return:
    """
    # Text is the written text in the Slack message excluding the /slash command
    # Example:  /misp_twitter <34 google.com>
    # <34 google.com> is a string.
    text = request.form['text']
    # Response_url is the callback to the Slack message and used to return data to the user.
    response_url = request.form['response_url']

    # Validate the input in text.  This may need to be changed given the number of args, type or data, etc.
    if valid_input(text):
        # First arg should always be a MISP Event ID.
        misp_event_id = text.split(" ")[0]
        # Second arg should always be a domain/URL.
        domain = text.split(" ")[1]
        # data is passed to the run function with the input text args + a response url so we can send data back.
        data = {
            'misp_event_id': misp_event_id,
            'domain': domain,
            'response_url': response_url
        }
        # Execute the task and add it the queue.
        q.enqueue(run, data)
        # Immediately return a message to the user notifying them of the job.
        resp = build_response('Adding {} tracking IDs to MISP Event {}.'.format(domain, misp_event_id))
        requests.post(response_url, json=resp)
    else:
        # If something blows up return an error to the user.
        resp = build_response('Invalid domain or MISP Event: {}'.format(text))
        requests.post(response_url, json=resp)
    # Return HTTP 200 on all post requests to this endpoint.
    return ('', 200)
