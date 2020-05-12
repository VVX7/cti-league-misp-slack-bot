import tweepy
from misp_objects import TrackingIDObject
from pymisp import ExpandedPyMISP, MISPEvent
from bs4 import BeautifulSoup
import requests
import json
import os
import re
import slack
import sys
from urllib.parse import urlsplit
import datetime

import logging

logger = logging.getLogger('log')

# Setup the Slack we client.
slack = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

# Initialize MISP API wrapper.
misp = ExpandedPyMISP(os.environ['MISP_URL'], os.environ['MISP_SECRET'], ssl=True)


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
    misp_event_id = text.split()[0]
    url = text.split()[1]
    # Regex matches a URL or domain.
    regex = re.compile(r"^(?:https?:\/\/)?([^\/|\?|\&|\$|\+|\,|\:|\;|\=|\@|\#]+)(?:\/.*)?$")
    match = regex.findall(url)

    try:
        # Verify that the MISP Event ID can be type cast to int() else it contains bad chars.
        # Verify that match contains at least 1 match and that url is therefore a valid domain/url.
        if int(misp_event_id) and len(match) > 0:
            return True
    except ValueError:
        return False


def get_builtwith_tracking_ids(domain):
    """
    Scrape BuiltWith for domain tracking ids and related domains.
    :param url:
    :return:
    """
    # Spoof the user-agent for the BuiltWith request.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    }

    # Try splitting the url and extracting the domain + tld only.
    # If the fails the domain was entered in a form we can pass directly to requests.
    url_split = urlsplit(domain)
    network_location = url_split.netloc
    if url_split.netloc == "":
        if "/" in domain:
            network_location = domain.split("/")[0]
        else:
            network_location = domain

    url = f"https://builtwith.com/relationships/{network_location}"

    # Set up the requests session and GET the BuiltWith page.
    session = requests.Session()
    response = session.get(url, headers=headers)
    # Parse the response into a bs4 object.
    soup = BeautifulSoup(response.content, 'html.parser')

    # tracking_ids stores the values we'll use to build the tracking-id MISP objects.
    # The structure of tracking_is is {<tracking id>: {"first-seen": "", "last-seen": "", "hostname": []}}
    # where hostname stores a list of domains using the tracking id.
    tracking_ids = {}

    # Scrape the tracking ids from this domain including their first/last seen time.
    for i in soup.find_all("tr", {"class": "tbomb"}):
        if i.get("id") is not None:
            tracking_ids[i.get("id")] = {}
            dates = i.find_all("td")
            tracking_ids[i.get("id")]['first-seen'] = dates[-2].get_text()
            tracking_ids[i.get("id")]['last-seen'] = dates[-1].get_text()
            tracking_ids[i.get("id")]['hostname'] = []
            tracking_ids[i.get("id")]['id'] = i.get("id")

    # Scrape the domains on which each tracking-id appears.
    for i in soup.find_all("td"):
        if i.get("relationships") is not None:
            ids = i.get("relationships").split("|")
            relationship = i.find("a").get_text()
            for each_id in ids:
                tracking_ids[each_id]['hostname'].append(relationship)

    return tracking_ids


def build_response(message, first=True):
    """
    Nothing to do here.
    This function builds a Slack response.
    "in_channel" specifies that the response should be visible to channel.
    :param message:
    :param first:
    :return:
    """
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
    Run() is executed and passed to the Redis queue. Therefore this function must execute all of the bot logic.
    :param data:
    :return:
    """
    misp_event_id = data['misp_event_id']
    domain = data['domain']
    response_url = data['response_url']

    try:
        # Get BuiltWith tracking IDs for the specified domain.
        # We're going to then use the returned dict to build tracking-id MISP objects.
        tracking_ids = get_builtwith_tracking_ids(domain)

        # Get the MISP event that the user specified in Slack.
        # pythonify=True means we want to convert the response to a PyMISP Event object (default response is json).
        working_event = misp.get_event(misp_event_id, extended=True, pythonify=True)

        # Load the misp object version from it's definition.json file.
        # PyMISP validates created objects against the misp-object schema.
        # Some objects are included by default in PyMISP but new objects will need to be accessed like this.
        with open("misp-objects/tracking-id/definition.json") as f:
            object_definition = json.load(f)
            f.close()

        # Create the MISP microblog object.
        # TODO: get the object definition from github
        # misp_objects_path_custom searches the var path for {objectname}/definition.json to load the object definition
        # This file needs to be updated when the upstream object is updated.
        #
        # Build the tracking-id objects.
        misp_objects = []
        for _, tracking_id in tracking_ids.items():
            tracking_id_object = TrackingIDObject(parameters=tracking_id,
                                                  misp_objects_path_custom="misp-objects",
                                                  template_version=str(object_definition["version"]))
            misp_objects.append(tracking_id_object)

        # Get the Slackbot's MISP org ID.
        # We do this because the bot can't modify anther org's events.
        user_profile = misp.get_user("me")
        bot_org_id = user_profile["User"]["org_id"]

        # If the bot org is the same and the MISP Event org we can update it directly.
        if str(bot_org_id) == str(working_event["org_id"]):
            for each_object in misp_objects:
                # Add each tracking_id_object to the event.
                working_event.Object.append(each_object)
            # Increment the event timestamp by 1 second to avoid timestamp collision.
            working_event.timestamp = working_event.timestamp + datetime.timedelta(seconds=1)
            result = misp.update_event(working_event)
            # Send the result to the docker container's stdout.
            print(result)
        else:
            # If the bot org is not the same as the event we're trying to modify then we need to use an extension.
            # Let's check if the bot already created an extension event for this event.
            new_event = True
            if "extensionEvents" in working_event:
                for k, event_extension in working_event["extensionEvents"].items():
                    # Checking if the org IDs match.
                    if event_extension["Orgc"]["id"] == bot_org_id:
                        # Check if the extension has the event name we expect this bot to create.
                        if event_extension["info"] == "Covid Slack: Disinfo Bot":
                            # Get the event and add the object we created.
                            extension_event = misp.get_event(event_extension["id"], pythonify=True)
                            for each_object in misp_objects:
                                extension_event.Object.append(each_object)
                            working_event.timestamp = working_event.timestamp + datetime.timedelta(seconds=1)
                            result = misp.update_event(extension_event)
                            # Send the result to the docker container's stdout.
                            print(result)
                            # Set new event false so we don't create a new event extension in the next step.
                            new_event = False
            # If the event isn't owned by the bot org , and no event extension exists, we need to create a new event.
            # This event will be added to the parent as an event extension.
            if new_event:
                # Create a new empty event.
                extended_event = MISPEvent()
                # Set self.info to row Title
                extended_event.info = "Covid Slack: Disinfo Bot"
                # extends_uuid tells us the event we are extending with this new event.
                extended_event.extends_uuid = working_event["id"]
                for tracking_id_object in misp_objects:
                    extended_event.Object.append(tracking_id_object)
                result = misp.add_event(extended_event, pythonify=True)
                print(result)

        # Build slack response.
        # This is the data posted back to the user in Slack.
        # Change 'text'['text'] to fit your bot name, etc.
        # 'response_type': 'in_channel' posts the response in channel. Remove response_type to make response private.
        response = {'blocks': [], 'response_type': 'in_channel'}
        response['blocks'].append({
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': 'BuiltWith Tracking IDs: {}'.format(domain)
            }
        })

        # Build the message line by line.
        # Requires explicit use of line break.
        message = ""
        for tracking_id, domains in tracking_ids.items():
            message += f'Tracking ID: {tracking_id}\n'
            message += f'Relationships: {str(len(domains["hostname"]))}\n'

        # Add Slack message as block.
        response['blocks'].append({
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': message
            }
        })

        # Finally, return the response to the user.
        requests.post(response_url, json=response)
    except Exception as e:
        # Return the error to the user and log to the container.
        logger.exception(f"Error: {e}")
        message = f"Error: {e}"
        resp = build_response(message, False)
        requests.post(response_url, json=resp)
