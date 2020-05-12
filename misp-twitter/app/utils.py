import tweepy
from misp_objects import MicroblogObject
from pymisp import ExpandedPyMISP, MISPEvent

import requests
import json
import os
import re
import slack
import datetime

import logging
logger = logging.getLogger('log')

slack = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

# Twitter OAuth.
auth = tweepy.OAuthHandler(consumer_key=os.environ['CONSUMER_KEY'], consumer_secret=os.environ['CONSUMER_SECRET'])
auth.set_access_token(key=os.environ['ACCESS_TOKEN'], secret=os.environ['ACCESS_TOKEN_SECRET'])

# Initialize Twitter API Client.
api = tweepy.API(auth)

# Initialize MISP API wrapper.
misp = ExpandedPyMISP(os.environ['MISP_URL'], os.environ['MISP_SECRET'], ssl=True)


def valid_input(text):
    """
    Verify that both the Twitter ID and MISP Event are integers.
    :param text:
    :return:
    """
    # Remove terminal whitespaces.
    text = text.strip()
    # Split on one or more whitespace
    misp_event_id = text.split()[0]
    twitter_post_id = text.split()[1]

    p = re.compile('twitter.com/[^/]+/status/([\d]+)')
    r = p.findall(twitter_post_id)

    try:
        if int(misp_event_id) and len(r) > 0:
            return True
        elif int(misp_event_id) and int(twitter_post_id):
            return True
    except ValueError:
        return False


def twitter_get_extended_status(status_id):
    """
    Get a Twitter status (Tweepy extended mode).
    :param status_id:
    :return:
    """
    p = re.compile('twitter.com/[^/]+/status/([\d]+)')
    r = p.findall(status_id)
    if len(r) > 0:
        try:
            response = api.get_status(r[0], tweet_mode="extended")
        except tweepy.error.TweepError as e:
            return str(e[0])
    else:
        try:
            response = api.get_status(status_id, tweet_mode="extended")
        except tweepy.error.TweepError as e:
            return str(e[0])
    return response


def escape_unicode(s):
    """
    Escape unicode characters.
    :param s:
    :return:
    """
    return s.encode("unicode-escape").decode("utf-8")


def transform_status_response(get_status_response):
    """
    Clean up the Tweepy status response into something that can be easily passed
    to the microblog MISP object.
    :param get_status_response:
    :return:
    """
    data = {}
    data["hashtag"] = []
    data["embedded-link"] = []
    data["username-quoted"] = []
    # Add the Twitter post content.
    # TODO: Twitter API truncates this. Find out how to get the full post.
    try:
        data["post"] = get_status_response["full_text"]

        # Add the Twitter post url.
        screen_name = get_status_response["user"]["screen_name"]
        post_id = get_status_response["id"]
        url = f"https://twitter.com/{screen_name}/status/{post_id}"
        data["url"] = url
    except KeyError:
        pass

    # Add hashtag(s).
    try:
        for hashtag in get_status_response["entities"]["hashtags"]:
            data["hashtag"].append(hashtag["text"])
    except KeyError:
        pass

    # Save to Internet Archive.
    # TODO: Save to Internet Archive.
    # try:
    #     archive = "foo"
    #     data["archive"] = archive
    # except KeyError:
    #     pass

    # The microblog type is 'Twitter'
    try:
        data["type"] = "Twitter"
    except KeyError:
        pass

    # Set the microblog state.
    # TODO: Use command line kwarg
    # try:
    #     data["state"] = "Disinformation"
    # except KeyError:
    #     pass

    # Add the Twitter username.
    try:
        data["username"] = get_status_response["user"]["screen_name"]
    except KeyError:
        pass

    # Add user display namme.
    try:
        data["display-name"] = get_status_response["user"]["name"]
    except KeyError:
        pass

    # Add the Twitter verification status.
    try:
        verified = get_status_response["user"]["verified"]
        if verified:
            data["verified-username"] = "Verified"
        else:
            data["verified-username"] = "Unverified"
    except KeyError:
        pass

    # Add embedded URL links(s).
    try:
        for url in get_status_response["entities"]["urls"]:
            data["embedded-link"].append(url["expanded_url"])
    except KeyError:
        pass
    # Add embedded twitter short links(s).
    try:
        for url in get_status_response["entities"]["urls"]:
            data["embedded-link"].append(url["url"])
    except KeyError:
        pass

    # Add embedded media links(s).
    try:
        for url in get_status_response["entities"]["media"]:
            data["embedded-link"].append(url["expanded_url"])
    except KeyError:
        pass
    # Add embedded twitter short links(s).
    try:
        for url in get_status_response["entities"]["media"]:
            data["embedded-link"].append(url["url"])
    except KeyError:
        pass

    # Add quoted username(s).
    try:
        for user in get_status_response["entities"]["user_mentions"]:
            data["username-quoted"].append(user["screen_name"])
    except KeyError:
        pass

    # Add post Twitter id.
    try:
        data["twitter-id"] = get_status_response["id_str"]
    except KeyError:
        pass

    # Add post content language.
    try:
        data["language"] = get_status_response["lang"]
    except KeyError:
        pass

    # Add in reply to user id.
    try:
        data["in-reply-to-user-id"] = get_status_response["in_reply_to_user_id_str"]
    except KeyError:
        pass

    # Add in reply to post id.
    try:
        data["in-reply-to-status-id"] = get_status_response["in_reply_to_status_id_str"]
    except KeyError:
        pass

    # Add post Twitter id.
    try:
        data["in-reply-to-display-name"] = get_status_response["in_reply_to_screen_name"]
    except KeyError:
        pass

    return data


def build_response(message, first=True):
    resp = {
        "text": message,
        "type": "mrkdwn"
    }

    if first:
        resp.update({'response_type': 'ephemeral'})
    else:
        resp.update({'replace_original': True})
    return resp


def run(data):
    """
    Do the things.
    :param data:
    :return:
    """
    misp_event_id = data['misp_event_id']
    twitter_post_id = data['twitter_post_id']
    response_url = data['response_url']

    try:
        # Get the Twitter status.
        status = twitter_get_extended_status(twitter_post_id)

        # Extract relevant values from the Twitter status.
        microblog_data = transform_status_response(status._json)

        # Load the microblog version from it's definition.json file.
        with open("misp-objects/microblog/definition.json") as f:
            microblog_definition = json.load(f)
            f.close()

        # Create the MISP mircroblog object.
        # TODO: get the object definition from github
        # misp_objects_path_custom searches the var path for {objectname}/definition.json to load the object definition
        # This file needs to be updated when the upstream object is updated.
        microblog = MicroblogObject(parameters=microblog_data,
                                    misp_objects_path_custom="misp-objects",
                                    template_version=str(microblog_definition["version"]))

        # Get the MISP event.
        working_event = misp.get_event(misp_event_id, extended=True, pythonify=True)

        # Get the Slackbot's MISP org ID.
        user_profile = misp.get_user("me")
        bot_org_id = user_profile["User"]["org_id"]

        # If the bot org can update the MISP Event with the new microblog do so.
        if str(bot_org_id) == str(working_event["org_id"]):
            working_event.Object.append(microblog)
            result = misp.update_event(working_event)
            print(result)
        else:
            new_event = True
            # If an extension exists for Slackbot objects use it.
            if "extensionEvents" in working_event:
                for k, event_extension in working_event["extensionEvents"].items():
                    if event_extension["Orgc"]["id"] == bot_org_id:
                        if event_extension["info"] == "Covid Slack: Disinfo Bot":
                            extension_event = misp.get_event(event_extension["id"], pythonify=True)
                            extension_event.Object.append(microblog)
                            result = misp.update_event(extension_event)
                            print(result)
                            new_event = False
            # Create a new extension to the parent event.
            if new_event:
                extended_event = MISPEvent()
                extended_event.info = "Covid Slack: Disinfo Bot"
                extended_event.extends_uuid = working_event["id"]
                extended_event.Object.append(microblog)
                result = misp.add_event(extended_event, pythonify=True)
                print(result)

        # Build slack response.
        response = {'blocks': [], 'response_type': 'in_channel'}
        response['blocks'].append({
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': 'Twitter Status: {}'.format(twitter_post_id)
            }
        })

        twitter_message = ""
        if microblog_data.get('username'):
            twitter_message += 'Username: {}\n'.format(microblog_data['username'])
        if microblog_data.get('display-name'):
            twitter_message += 'Display Name: {}\n'.format(microblog_data['display-name'])
        if microblog_data.get('verified'):
            twitter_message += 'Verified Account: {}\n'.format(microblog_data['verified'])
        if microblog_data.get('post'):
            twitter_message += 'Status: {}\n'.format(microblog_data['post'])
        if microblog_data.get('in-reply-to-user-id'):
            twitter_message += 'In-Reply-To User ID: {}\n'.format(microblog_data['in-reply-to-user-id'])
        if microblog_data.get('in-reply-to-status-id'):
            twitter_message += 'In-Reply-To Status ID: {}\n'.format(microblog_data['in-reply-to-status-id'])
        if microblog_data.get('in-reply-to-display-name'):
            twitter_message += 'In-Reply-To Display Name: {}\n'.format(microblog_data['in-reply-to-display-name'])
        if microblog_data.get('language'):
            twitter_message += 'Language: {}\n'.format(microblog_data['language'])

        if len(microblog_data['hashtag']) > 0:
            twitter_message += 'Hashtags:\n'
            for hashtag in microblog_data['hashtag']:
                twitter_message += '* {}\n'.format(hashtag)

        if len(microblog_data['embedded-link']) > 0:
            twitter_message += 'Embedded URLs:\n'
            for url in microblog_data['embedded-link']:
                twitter_message += '* {}\n'.format(url)

        if len(microblog_data['username-quoted']) > 0:
            twitter_message += 'Quoted Usernames:\n'
            for name in microblog_data['username-quoted']:
                twitter_message += '* {}\n'.format(name)

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
        logger.exception("twitter_microblog exception:")
        message = "An error has occurred!"
        resp = build_response(message, False)
        requests.post(response_url, json=resp)
