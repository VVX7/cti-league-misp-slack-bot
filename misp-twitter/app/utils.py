import tweepy
from misp_objects import MicroblogObject, TwitterAccountObject, TwitterPostObject
from pymisp import ExpandedPyMISP, MISPEvent

import requests
import json
import os
import re
import slack
import base64
from urllib.parse import urlparse
import datetime
import traceback
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger = logging.getLogger('log')

slack = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

# Twitter OAuth.
auth = tweepy.OAuthHandler(consumer_key=os.environ['CONSUMER_KEY'], consumer_secret=os.environ['CONSUMER_SECRET'])
auth.set_access_token(key=os.environ['ACCESS_TOKEN'], secret=os.environ['ACCESS_TOKEN_SECRET'])

# Initialize Twitter API Client.
api = tweepy.API(auth)

# Initialize MISP API wrapper.
misp = ExpandedPyMISP(os.environ['MISP_URL'], os.environ['MISP_SECRET'], ssl=True)


def valid_twitter_post(text):
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


def valid_twitter_account(text):
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

    p = re.compile('twitter.com/([^/]+)')
    r = p.findall(twitter_post_id)

    try:
        if int(misp_event_id) and len(r) > 0:
            return True
        elif int(misp_event_id) and int(twitter_post_id):
            return True
    except ValueError:
        return False


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


def twitter_get_post(status_id):
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


def twitter_get_account(status_id):
    """
    Get a Twitter status (Tweepy extended mode).
    :param status_id:
    :return:
    """
    p = re.compile('twitter.com/([^/]+)')
    r = p.findall(status_id)
    if len(r) > 0:
        try:
            response = api.get_user(r[0], tweet_mode="extended")
        except tweepy.error.TweepError as e:
            return str(e[0])
    else:
        try:
            response = api.get_user(status_id, tweet_mode="extended")
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


def return_file_name(url):
    try:
        a = urlparse(url)
        file_name = a.path.split("/")[-1]
        return file_name
    except:
        return None

def return_banner_name(url):
    try:
        file_name = url.split("/")[-1]
        return file_name
    except:
        return None

def return_b64_attachement(url):
    try:
        attachment = requests.get(url)
        b64_attachment = base64.b64encode(attachment.content)
        return b64_attachment
    except:
        return None


def return_iso_timestamp(epoch_time):
    return datetime.datetime.utcfromtimestamp(epoch_time).isoformat()


def return_hashtags(comment):
    p = re.compile('(?<![/\w+])#(\w+)')
    r = p.findall(comment)
    return r


def transform_twitter_post(response):
    """
    Clean up the Tweepy status response into something that can be easily passed
    to the microblog MISP object.
    :param get_status_response:
    :return:
    """
    data = {}
    data["attachment"] = []
    data["hashtag"] = []
    data["embedded-link"] = []
    data["username-quoted"] = []

    # data['first_seen'] = return_iso_timestamp(response.created_at)

    # Add images in Tweet
    try:
        for i in response["extended_entities"]["media"]:
            name = return_file_name(i["media_url"])
            attachment = return_b64_attachement(i["media_url"])
            data['attachment'].append({"filename": name, "data": attachment})
    except Exception as e:
        logger.exception(e)
        pass

    # Add embedded URL links(s).
    try:
        for url in response["entities"]["urls"]:
            data["embedded-link"].append(url["expanded_url"])
    except KeyError:
        pass

    # Add the Twitter username.
    try:
        data["favorite-count"] = response["favorite_count"]
    except KeyError:
        pass

    # Add the Twitter username.
    try:
        if response["geo"]:
            data["geo"] = response["geo"]
    except KeyError:
        pass

    # Add hashtag(s).
    try:
        for hashtag in response["entities"]["hashtags"]:
            data["hashtag"].append(hashtag["text"])
    except KeyError:
        pass

    # Add in reply to user id.
    try:
        data["in-reply-to-user-id"] = response["in_reply_to_user_id_str"]
    except KeyError:
        pass

    # Add in reply to post id.
    try:
        data["in-reply-to-status-id"] = response["in_reply_to_status_id_str"]
    except KeyError:
        pass

    # Add post Twitter id.
    try:
        data["in-reply-to-display-name"] = response["in_reply_to_screen_name"]
    except KeyError:
        pass

    # Add post content language.
    try:
        data["language"] = response["lang"]
    except KeyError:
        pass

    # Link to original post.
    try:
        data["link"] = f"https://twitter.com/{response['user']['screen_name']}/status/{response['id']}"
    except KeyError:
        pass

    # Add user display namme.
    try:
        data["name"] = response["user"]["name"]
    except KeyError:
        pass

    # Add possibly_sensitive
    try:
        data["possibly-sensitive"] = response["possibly_sensitive"]
    except KeyError:
        pass

    # Add possibly_sensitive_appealable
    try:
        data["possibly-sensitive-appealable"] = response["possibly_sensitive_appealable"]
    except KeyError:
        pass

    # Add the Twitter post content.
    try:
        data["post"] = response["full_text"]
    except KeyError:
        pass

    # Add the Twitter ID
    try:
        data["post-id"] = response["id"]
    except KeyError:
        pass

    # Add the retweet count
    try:
        data["retweet-count"] = response["retweet_count"]
    except KeyError:
        pass

    # source of tweet
    try:
        data["source"] = response["source"]
    except KeyError:
        pass

    # Link to original post.
    try:
        data["user-id"] = response["user"]["id_str"]
    except KeyError:
        pass

    # Add quoted username(s).
    try:
        for user in response["entities"]["user_mentions"]:
            data["username-quoted"].append(user["screen_name"])
    except KeyError:
        pass

    return data


def transform_twitter_account(response):
    data = {}
    data["embedded-link"] = []
    data["hashtag"] = []
    data["profile-image"] = []

    # Bio
    try:
        data["bio"] = response["description"]
    except KeyError:
        pass

    # display name
    try:
        data["displayed-name"] = response["name"]
    except KeyError:
        pass

    # Bio
    try:
        for i in response["entities"]["url"]["urls"]:
            data["embedded-link"].append(i["expanded_url"])
    except KeyError:
        pass

    # display name
    try:
        data["followers"] = response["followers_count"]
    except KeyError:
        pass

    # display name
    try:
        data["following"] = response["following"]
    except KeyError:
        pass

    # Add description hashtag(s).
    try:
        hashtags = return_hashtags(response["description"])
        for hashtag in hashtags:
            data["hashtag"].append(hashtag)
    except KeyError:
        pass

    # Add username hashtag(s).
    try:
        name_hashtags = return_hashtags(response["name"])
        for hashtag in name_hashtags:
            data["hashtag"].append(hashtag)
    except KeyError:
        pass

    # display name id
    try:
        data["id"] = response["id_str"]
    except KeyError:
        pass

    # display name
    try:
        data["likes"] = response["favourites_count"]
    except KeyError:
        pass

    # link to user
    try:
        data["link"] = f"https://twitter.com/{response['screen_name']}"
    except KeyError:
        pass

    # number of lists the user is on
    try:
        data["listed"] = response["listed_count"]
    except KeyError:
        pass

    # location
    try:
        data["location"] = response["location"]
    except KeyError:
        pass

    # name
    try:
        data["name"] = response["name"]
    except KeyError:
        pass

    # private
    try:
        if response["protected"]:
            data["protected"] = "True"
        else:
            data["protected"] = "False"
    except KeyError:
        pass

    # Add images in Tweet
    try:
        banner_name = return_banner_name(response["profile_banner_url"])
        logger.info(f"Banner name: {banner_name}")
        banner_attachment = return_b64_attachement(response["profile_banner_url"])
        logger.info(f"Banner attachement: {banner_attachment}")
        data['profile-banner'] = {"filename": banner_name, "data": banner_attachment}
    except Exception as e:
        logger.exception(e)
        pass

    # location
    try:
        data["profile-banner-url"] = response["profile_banner_url"]
    except KeyError:
        pass

    # Add images in Tweet
    try:
        avatar_name = return_file_name(response["profile_image_url_https"])
        logger.info(f"Banner name: {avatar_name}")
        avatar_attachment = return_b64_attachement(response["profile_image_url_https"])
        logger.info(f"Banner name: {avatar_attachment}")
        data['profile-image'].append({"filename": avatar_name, "data": avatar_attachment})
    except Exception as e:
        logger.exception(e)
        pass

    # location
    try:
        data["profile-image-url"] = response["profile_image_url_https"]
    except KeyError:
        pass

    # tweets
    try:
        data["tweets"] = response["statuses_count"]
    except KeyError:
        pass

    # Add the Twitter verification status.
    try:
        verified = response["user"]["verified"]
        if verified:
            data["verified-username"] = "Verified"
        else:
            data["verified-username"] = "Unverified"
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


def twitter_post(data):
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
        status = twitter_get_post(twitter_post_id)

        # Extract relevant values from the Twitter status.
        microblog_data = transform_twitter_post(status._json)

        # Load the microblog version from it's definition.json file.
        with open("misp-objects/twitter-post/definition.json") as f:
            microblog_definition = json.load(f)
            f.close()

        # Create the MISP mircroblog object.
        # TODO: get the object definition from github
        # misp_objects_path_custom searches the var path for {objectname}/definition.json to load the object definition
        # This file needs to be updated when the upstream object is updated.
        microblog = TwitterPostObject(parameters=microblog_data,
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
        if microblog_data.get('name'):
            twitter_message += 'Username: {}\n'.format(microblog_data['name'])
        if microblog_data.get('verified'):
            twitter_message += 'Verified Account: {}\n'.format(microblog_data['verified'])
        if microblog_data.get('in-reply-to-user-id'):
            twitter_message += 'In-Reply-To User ID: {}\n'.format(microblog_data['in-reply-to-user-id'])
        if microblog_data.get('in-reply-to-status-id'):
            twitter_message += 'In-Reply-To Status ID: {}\n'.format(microblog_data['in-reply-to-status-id'])
        if microblog_data.get('in-reply-to-display-name'):
            twitter_message += 'In-Reply-To Display Name: {}\n'.format(microblog_data['in-reply-to-display-name'])

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
        logger.info(traceback.print_exc(file=sys.stdout))
        message = "An error has occurred!"
        resp = build_response(message, False)
        requests.post(response_url, json=resp)


def twitter_account(data):
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
        status = twitter_get_account(twitter_post_id)

        # Extract relevant values from the Twitter status.
        microblog_data = transform_twitter_account(status._json)

        # Load the microblog version from it's definition.json file.
        with open("misp-objects/twitter-account/definition.json") as f:
            microblog_definition = json.load(f)
            f.close()

        # Create the MISP mircroblog object.
        # TODO: get the object definition from github
        # misp_objects_path_custom searches the var path for {objectname}/definition.json to load the object definition
        # This file needs to be updated when the upstream object is updated.
        microblog = TwitterAccountObject(parameters=microblog_data,
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
        if microblog_data.get('name'):
            twitter_message += 'Username: {}\n'.format(microblog_data['name'])
        if microblog_data.get('display-name'):
            twitter_message += 'Display Name: {}\n'.format(microblog_data['display-name'])
        if microblog_data.get('verified'):
            twitter_message += 'Verified Account: {}\n'.format(microblog_data['verified'])
        if microblog_data.get('description'):
            twitter_message += 'Bio: {}\n'.format(microblog_data['description'])

        if len(microblog_data['hashtag']) > 0:
            twitter_message += 'Hashtags:\n'
            for hashtag in microblog_data['hashtag']:
                twitter_message += '* {}\n'.format(hashtag)

        if len(microblog_data['embedded-link']) > 0:
            twitter_message += 'Embedded URLs:\n'
            for url in microblog_data['embedded-link']:
                twitter_message += '* {}\n'.format(url)

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
        logger.info(traceback.print_exc(file=sys.stdout))
        message = "An error has occurred!"
        resp = build_response(message, False)
        requests.post(response_url, json=resp)
