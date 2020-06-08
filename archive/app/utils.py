import requests
import os
import re
import slack
import time

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

slack = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

IA_KEY = os.environ['IA_KEY']
IA_SECRET = os.environ['IA_SECRET']

class WayBack:
    def __init__(self, IA_KEY, IA_SECRET):
        self.IA_KEY = IA_KEY
        self.IA_SECRET = IA_SECRET
        self.headers = {"Accept": "application/json",
                        "Authorization": f"LOW {self.IA_KEY}:{self.IA_SECRET}"}

    def save_page(self, url):
        """
        Returns status ID.
        :param url:
        :return:
        """
        data = {"url": f"{url}",
                "capture_all": 1,
                "capture_outlinks": 1,
                "capture_screenshot": 1}

        r = requests.post("https://web.archive.org/save", headers=self.headers, data=data)
        return r.json()

    def check_status(self, status):
        job_id = status["job_id"]
        r = requests.get(f"https://web.archive.org/save/status/{job_id}", headers=self.headers)
        status = r.json()
        print(status)
        while status["status"] != "success":
            if status["status"] == "error":
                return r.json()
            time.sleep(10)
            r = requests.get(f"https://web.archive.org/save/status/{job_id}", headers=self.headers)
            status = r.json()
        return r.json()

    def return_archive_urls(self, status):
        timestamp = status["timestamp"]
        original_url = status["original_url"]
        archive = f"https://web.archive.org/web/{timestamp}/{original_url}"
        return archive


def valid_input(text):
    """
    Validates the Slack message.
    This function needs to be changed to suit the desired input of your bot.
    :param text:  The user input from Slack.
    :return: bool
    """
    # Remove leading/trailing whitespaces.
    text = text.strip()
    # Split on one or more whitespaces in the text.
    url = text.split()[0]
    # Regex matches a URL or domain.
    regex = re.compile(r"^(?:https?:\/\/)?([^\/|\?|\&|\$|\+|\,|\:|\;|\=|\@|\#]+)(?:\/.*)?$")
    match = regex.findall(url)

    try:
        # Verify that the MISP Event ID can be type cast to int() else it contains bad chars.
        # Verify that match contains at least 1 match and that url is therefore a valid domain/url.
        if len(url) > 0:
            return True
    except ValueError:
        return False




def build_response(message, first=True):
    resp = {
        "text": message,
        "type": "mrkdwn"
    }

    if first:
        resp.update({'response_type': 'in_channel'})
    else:
        resp.update({'replace_original': True})
    return resp


def run(data):
    """
    Do the things.
    :param data:
    :return:
    """
    archive_url = data['archive_url']
    response_url = data['response_url']

    try:

        wayback = WayBack(IA_KEY=IA_KEY, IA_SECRET=IA_SECRET)
        request = wayback.save_page(archive_url)
        status = wayback.check_status(request)
        archive_urls = wayback.return_archive_urls(status)

        # Build slack response.
        response = {'blocks': [], 'response_type': 'in_channel'}
        response['blocks'].append({
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': 'Internet Archive'
            }
        })

        twitter_message = ""
        twitter_message += 'Archive: {}\n'.format(archive_urls)


        # Add Twitter message as block.
        response['blocks'].append({
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': twitter_message
            }
        })

        requests.post(response_url, json=response)
    except Exception:
        logger.exception("Archive exception:")
        message = "An error has occurred!"
        resp = build_response(message, False)
        requests.post(response_url, json=resp)
