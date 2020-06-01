from misp_objects import RedditAccount, RedditPost, RedditComment, RedditSubReddit
from pymisp import ExpandedPyMISP, MISPEvent
from prawcore.exceptions import NotFound

import requests
import json
import praw
import os
import re
import slack
import datetime
import traceback
import sys

import logging
logger = logging.getLogger('log')

#slack = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

# Initialize MISP API wrapper.
misp = ExpandedPyMISP(os.environ['MISP_URL'], os.environ['MISP_SECRET'], ssl=True)

#Initialize reddit library
reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'], client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                     password=os.environ['REDDIT_PASSWORD'], user_agent='CTI-League Reddit User',
                     username=os.environ['REDDIT_USER'])

def valid_reddit_account(text):
    """
    Verify that a valid reddit username and MISP event are sent
    """

    text = text.strip()

    try:
        misp_event_id = text.split()[0]
        reddit_user = text.split()[1]
    except IndexError:
        return False

    p = re.compile('[A-Za-z0-9_-]+')
    m = p.match(reddit_user)

    try:
        if int(misp_event_id) and m is not None:
            return True
        else:
            return False
    except ValueError:
        return False


def valid_subreddit(text):
    """
    Verify that both the subreddit URL and MISP Event are valid
    """
    text = text.strip()
    misp_event_id = text.split()[0]
    subreddit_url = text.split()[1]

    p = re.compile('reddit.com/r/[^/]+')
    r = p.findall(subreddit_url)

    try:
        if int(misp_event_id) and len(r) > 0:
            return True
        else:
            return False
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
    try:
        misp_event_id = text.split()[0]
        twitter_post_id = text.split()[1]
    except IndexError:
        return False

    p = re.compile('twitter.com/[^/]+/status/([\d]+)')
    r = p.findall(twitter_post_id)

    try:
        if int(misp_event_id) and len(r) > 0:
            return True
        elif int(misp_event_id) and int(twitter_post_id):
            return True
    except ValueError:
        return False


def escape_unicode(s):
    """
    Escape unicode characters.
    :param s:
    :return:
    """
    return s.encode("unicode-escape").decode("utf-8")


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

def process_reddit_subreddit(data):
    """
    Get data on a subreddit
    :param data:
    :return:
    """
    misp_event_id = data['misp_event_id']
    reddit_subreddit = data['reddit_subreddit']
    response_url = data['response_url']

    try:
        subreddit = reddit.subreddit(reddit_subreddit)
        with open('misp-objects/reddit-subreddit/definition.json') as f:
            reddit_subreddit_definition = json.load(f)
            f.close()

        reddit_subreddit_data = transform_reddit_subreddit(subreddit)
        reddit_subreddit = RedditSubReddit(parameters=reddit_subreddit_data, misp_objects_path_custom='misp-objects',
                                           template_version=str(reddit_subreddit_definition['version']))

        #Get the MISP event
        working_event = misp.get_event(misp_event_id, extended=True, pythonify=True)

        # Get the slackbot's MISP ID
        user_profile = misp.get_user('me')
        bot_org_id = user_profile['User']['org_id']

        if str(bot_org_id) == str(working_event['org_id']):
            working_event.Object.append(reddit_subreddit)
            result = misp.update_event(working_event)
            print(result)
        else:
            new_event = True
            if 'extensionevents' in working_event:
                for k, event_extension in working_event['extensionEvents'].items():
                    if event_extension['Orgc']['id'] == bot_org_id:
                        if event_extension['info'] == 'Covid Slack: Disinfo Bot':
                            extension_event = misp.get_event(event_extension['id'], pythonify=True)
                            extension_event.Object.append(reddit_subreddit)
                            result = misp.update_event(extension_event)
                            print(result)
                            new_event = False

            if new_event:
                extended_event = MISPEvent()
                extended_event.info = 'Covid Slack: Disinfo Bot'
                extended_event.extends_uuid = working_event['id']
                extended_event.Object.append(reddit_subreddit)
                result = misp.add_event(extended_event, pythonify=True)
                print(result)


        #Build slack response
        response = {'blocks' : [], 'response_type': 'in_channel'}
        response['blocks'].append({
                                   'type' : 'section',
                                   'text': {
                                       'type' : 'mrkdwn',
                                       'text' : 'Reddit Subreddit Status: {}'.format(reddit_subreddit_data['link'])
                                   }
        })

        message = reddit_subreddit_data['description']

        response['blocks'].append({
                                   'type' : 'section',
                                   'text' : {
                                       'type' : 'mrkdwn',
                                       'text' : message
                                   }
        })

        requests.post(response_url, json=response)
    except:
        traceback.print_exc(file=sys.stdout)
        resp = build_response(f'Reddit subreddit {reddit_subreddit} not found')
        requests.post(url=response_url, json=resp)


def process_reddit_post(data):
    """
    Get data on a reddit post
    :param data:
    :return:
    """
    misp_event_id = data['misp_event_id']
    reddit_post_id = data['reddit_post_id']
    response_url = data['response_url']

    try:
        submission = reddit.submission(reddit_post_id)
        with open('misp-objects/reddit-post/definition.json') as f:
            reddit_post_definition = json.load(f)
            f.close()

        reddit_post_data = transform_reddit_post(submission)
        reddit_post = RedditPost(
                                       parameters=reddit_post_data,
                                       misp_objects_path_custom='misp-objects',
                                       template_version=str(reddit_post_definition['version'])
        )

        #Get the MISP event
        working_event = misp.get_event(misp_event_id, extended=True, pythonify=True)

        # Get the slackbot's MISP ID
        user_profile = misp.get_user('me')
        bot_org_id = user_profile['User']['org_id']

        if str(bot_org_id) == str(working_event['org_id']):
            working_event.Object.append(reddit_post)
            result = misp.update_event(working_event)
            print(result)
        else:
            new_event = True
            if 'extensionevents' in working_event:
                for k, event_extension in working_event['extensionEvents'].items():
                    if event_extension['Orgc']['id'] == bot_org_id:
                        if event_extension['info'] == 'Covid Slack: Disinfo Bot':
                            extension_event = misp.get_event(event_extension['id'], pythonify=True)
                            extension_event.Object.append(reddit_post)
                            result = misp.update_event(extension_event)
                            print(result)
                            new_event = False

            if new_event:
                extended_event = MISPEvent()
                extended_event.info = 'Covid Slack: Disinfo Bot'
                extended_event.extends_uuid = working_event['id']
                extended_event.Object.append(reddit_post)
                result = misp.add_event(extended_event, pythonify=True)
                print(result)


        #Build slack response
        response = {'blocks' : [], 'response_type': 'in_channel'}
        response['blocks'].append({
                                   'type' : 'section',
                                   'text': {
                                       'type' : 'mrkdwn',
                                       'text' : 'Reddit Post Status: {}'.format(reddit_post_data['link'])
                                   }
        })

        message = reddit_post_data['description']

        response['blocks'].append({
                                   'type' : 'section',
                                   'text' : {
                                       'type' : 'mrkdwn',
                                       'text' : message
                                   }
        })

        requests.post(response_url, json=response)
    except:
        traceback.print_exc(file=sys.stdout)
        resp = build_response(f'Reddit post {reddit_post_id} not found')
        requests.post(url=response_url, json=resp)


def process_reddit_comment(data):
    """
    Get data on a reddit comment
    :param data:
    :return:
    """

    misp_event_id = data['misp_event_id']
    reddit_comment_id = data['reddit_comment_id']
    response_url = data['response_url']

    try:
        comment = reddit.comment(reddit_comment_id)
        with open('misp-objects/reddit-comment/definition.json') as f:
            reddit_comment_definition = json.load(f)
            f.close()

        reddit_comment_data = transform_reddit_comment(comment)
        reddit_comment = RedditComment(
                                       parameters=reddit_comment_data,
                                       misp_objects_path_custom='misp-objects',
                                       template_version=str(reddit_comment_definition['version'])
        )

        #Get the MISP event
        working_event = misp.get_event(misp_event_id, extended=True, pythonify=True)

        # Get the slackbot's MISP ID
        user_profile = misp.get_user('me')
        bot_org_id = user_profile['User']['org_id']

        if str(bot_org_id) == str(working_event['org_id']):
            working_event.Object.append(reddit_comment)
            result = misp.update_event(working_event)
            print(result)
        else:
            new_event = True
            if 'extensionevents' in working_event:
                for k, event_extension in working_event['extensionEvents'].items():
                    if event_extension['Orgc']['id'] == bot_org_id:
                        if event_extension['info'] == 'Covid Slack: Disinfo Bot':
                            extension_event = misp.get_event(event_extension['id'], pythonify=True)
                            extension_event.Object.append(reddit_comment)
                            result = misp.update_event(extension_event)
                            print(result)
                            new_event = False

            if new_event:
                extended_event = MISPEvent()
                extended_event.info = 'Covid Slack: Disinfo Bot'
                extended_event.extends_uuid = working_event['id']
                extended_event.Object.append(reddit_comment)
                result = misp.add_event(extended_event, pythonify=True)
                print(result)


        #Build slack response
        response = {'blocks' : [], 'response_type': 'in_channel'}
        response['blocks'].append({
                                   'type' : 'section',
                                   'text': {
                                       'type' : 'mrkdwn',
                                       'text' : 'Reddit Comment Status: {}'.format(reddit_comment_data['link'])
                                   }
        })

        message = reddit_comment_data['description']

        response['blocks'].append({
                                   'type' : 'section',
                                   'text' : {
                                       'type' : 'mrkdwn',
                                       'text' : message
                                   }
        })

        requests.post(response_url, json=response)
    except:
        traceback.print_exc(file=sys.stdout)
        resp = build_resonse(f'Reddit comment {reddit_comment_id} not found')
        requests.post(response_url, json=resp)

def process_reddit_account(data):
    """
    Get data on reddit Account
    :param data:
    :return:
    """

    misp_event_id = data['misp_event_id']
    reddit_account_name = data['reddit_account']
    response_url = data['response_url']

    try:
        redditor = reddit.redditor(reddit_account_name)

        with open('misp-objects/reddit-account/definition.json') as f:
            reddit_account_definition = json.load(f)
            f.close()

        reddit_account_data = transform_reddit_account(redditor)

        reddit_account = RedditAccount(parameters=reddit_account_data,
                                       misp_objects_path_custom='misp-objects',
                                       template_version=str(reddit_account_definition['version']))

        #Get the MISP event
        working_event = misp.get_event(misp_event_id, extended=True, pythonify=True)

        # Get the slackbot's MISP ID
        user_profile = misp.get_user('me')
        bot_org_id = user_profile['User']['org_id']

        if str(bot_org_id) == str(working_event['org_id']):
            working_event.Object.append(reddit_account)
            result = misp.update_event(working_event)
            print(result)
        else:
            new_event = True
            if 'extensionevents' in working_event:
                for k, event_extension in working_event['extensionEvents'].items():
                    if event_extension['Orgc']['id'] == bot_org_id:
                        if event_extension['info'] == 'Covid Slack: Disinfo Bot':
                            extension_event = misp.get_event(event_extension['id'], pythonify=True)
                            extension_event.Object.append(reddit_account)
                            result = misp.update_event(extension_event)
                            print(result)
                            new_event = False

            if new_event:
                extended_event = MISPEvent()
                extended_event.info = 'Covid Slack: Disinfo Bot'
                extended_event.extends_uuid = working_event['id']
                extended_event.Object.append(reddit_account)
                result = misp.add_event(extended_event, pythonify=True)
                print(result)


        #Build slack response
        response = {'blocks' : [], 'response_type': 'in_channel'}
        response['blocks'].append({
                                   'type' : 'section',
                                   'text': {
                                       'type' : 'mrkdwn',
                                       'text' : f'Reddit Account Status: {reddit_account_name}'
                                   }
        })

        message = reddit_account_data['description']

        response['blocks'].append({
                                   'type' : 'section',
                                   'text' : {
                                       'type' : 'mrkdwn',
                                       'text' : message
                                   }
        })

        requests.post(response_url, json=response)
    except:
        traceback.print_exc(file=sys.stdout)
        resp = build_response(f'Reddit user {reddit_account} not found')
        requests.post(url=resonse_url, json=resp)

def transform_reddit_account(redditor):
    data = {}
    data['account-avatar'] = []
    data['archive'] = []
    data['attachment'] = []
    data['moderator-of'] = []
    data['trophies'] = []
    data['user-avatar'] = []

    data['account-avatar'] = redditor.subreddit['banner_img']
    data['account-id'] = redditor.id
    data['account-name'] = redditor.name
    description = f'ID {redditor.id} Name {redditor.name}'
    data['description'] = description
    subreddits = []
    for subreddit in redditor.moderated():
         subreddits.append(subreddit.display_name)
    data['moderator-of'] = subreddits

    trophies = []
    for trophy in redditor.trophies():
         trophies.append(trophy.name)

    data['trophies'] = trophies
    data['link'] = f'https://reddit.com/user/{redditor.name}/'
    data['url'] = data['link']

    data['user-avatar'] = redditor.icon_img


    return data

def transform_reddit_comment(comment):
    data = {}
    data['archive'] = []
    data['attachment'] = []

    data['comment'] = comment.body
    data['creator'] = comment.author.name

    description = f'Created {comment.created_utc} distinguished: {comment.distinguished} parent_id: {comment.parent_id}'
    description += f' score: {comment.score} stickied: {comment.stickied} edited: {comment.edited}'

    data['description'] = description
    data['embedded-link'] = return_embedded_links(comment.body)
    data['hashtag'] = return_hashtags(comment.body)
    link = f'https://reddit.com/{comment.permalink}'
    data['link'] = link
    data['subreddit-name'] = return_subreddit(comment.permalink)

    data['url'] = link
    data['username-quoted'] = return_embedded_users(comment.body)
    return data

def transform_reddit_post(post):
    data = {}
    data['archive'] = []
    data['attachment'] = []

    data['creator'] = post.author.name

    description = f'Created {post.created_utc} distinguished: {post.distinguished} locked: {post.locked}'
    description += f' Comments: {post.num_comments} Score: {post.score} Stickied: {post.stickied} Upvote ratio: {post.upvote_ratio}'

    data['description'] = description

    if len(post.selftext) > 0:
        data['embedded-link'] = return_embedded_links(post.selftext)
        data['hashtag'] = return_hashtags(post.selftext)
        data['post-content'] = post.selftext
        data['username-quoted'] = return_embedded_users(post.selftext)
    else:
        data['embedded-link'] = [post.url]
        data['post-content'] = post.url

    data['link'] = f'https://reddit.com/{post.permalink}'
    data['post-title'] = post.title
    data['url'] = data['link']
    data['subreddit-name'] = return_subreddit(post.permalink)

    return data

def transform_reddit_subreddit(subreddit):
    data = {}
    data['archive'] = []
    data['attachment'] = []

    data['community-icon'] = subreddit.icon_img
    moderators = []
    for moderator in subreddit.moderator():
        moderators.append(moderator)

    data['creator'] = moderators[0]

    data['description'] = subreddit.public_description
    data['embedded-link'] = return_embedded_links(subreddit.description)
    data['hashtag'] = return_hashtags(subreddit.description)
    data['header-image'] = subreddit.header_img
    data['link'] = f'https://reddit.com{subreddit.url}'
    data['url'] = data['link']
    data['moderator'] = moderators

    if subreddit.allow_discovery:
        data['privacy'] = 'Public'
    else:
        data['privacy'] = 'Private'

    rules=subreddit.rules()
    data['rules'] = rules['rules']

    r=requests.get(f'https://reddit.com{subreddit.url}')

    if r.status_code == 200:
        data['submit-text'] = r.text

    data['subreddit-name'] = subreddit.display_name
    data['subreddit-type'] = subreddit.subreddit_type
    return data




def return_embedded_links(comment):
    p = re.compile('\[.*\]\((.*)\)')
    r = p.findall(comment)
    return r

def return_hashtags(comment):
    p = re.compile('#(\w+)')
    r = p.findall(comment)
    return r

def return_subreddit(permalink):
    p = re.compile('/r/[^/]+/')
    r = p.findall(permalink)[0]
    r = r.replace('/r/', '')
    r = r.replace('/', '')
    return r

def return_embedded_users(comment):
    p = re.compile('u/(\w+)')
    r = p.findall(comment)
    return r
