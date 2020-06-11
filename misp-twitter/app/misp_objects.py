#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymisp.tools.abstractgenerator import AbstractMISPObjectGenerator


class TwitterPostObject(AbstractMISPObjectGenerator):

    def __init__(self, parameters: dict, strict: bool = True, standalone: bool = True, **kwargs):
        super(TwitterPostObject, self).__init__('twitter-post', strict=strict, standalone=standalone, **kwargs)
        self._parameters = parameters
        self.generate_attributes()

    def generate_attributes(self):
        # Archive of the original document (Internet Archive, Archive.is, etc).
        if self._parameters.get('archive'):
            if type(self._parameters.get('archive')) is list:
                for i in self._parameters.get('archive'):
                    self.add_attribute('archive', value=i)
            else:
                self.add_attribute('archive', value=self._parameters['archive'])

        # attachment
        if self._parameters.get('attachment'):
            if type(self._parameters.get('attachment')) is list:
                for i in self._parameters.get('attachment'):
                    self.add_attribute('attachment',
                                       value=i["filename"], data=i["data"])
            else:
                self.add_attribute('attachment',
                                   value=self._parameters.get('attachment')["filename"],
                                   data=self._parameters.get('attachment')["data"])

        # embedded-link.
        if self._parameters.get('embedded-link'):
            if type(self._parameters.get('embedded-link')) is list:
                for i in self._parameters.get('embedded-link'):
                    self.add_attribute('embedded-link', value=i)
            else:
                self.add_attribute('embedded-link', value=self._parameters['embedded-link'])

        # embedded-safe-link
        if self._parameters.get('embedded-safe-link'):
            if type(self._parameters.get('embedded-safe-link')) is list:
                for i in self._parameters.get('embedded-safe-link'):
                    self.add_attribute('embedded-safe-link', value=i)
            else:
                self.add_attribute('embedded-safe-link', value=self._parameters['embedded-safe-link'])

        # Favorite count at time of archive.
        if self._parameters.get('favorite-count'):
            self.add_attribute('favorite-count', value=self._parameters['favorite-count'])

        # Geo data
        if self._parameters.get('geo'):
            self.add_attribute('geo', value=self._parameters['geo'])

        # Hashtag into the microblog post.
        if self._parameters.get('hashtag'):
            if type(self._parameters.get('hashtag')) is list:
                for i in self._parameters.get('hashtag'):
                    self.add_attribute('hashtag', value=i)
            else:
                self.add_attribute('hashtag', value=self._parameters['hashtag'])

        # The user ID of the microblog this post replies to.
        if self._parameters.get('in-reply-to-user-id'):
            if type(self._parameters.get('in-reply-to-user-id')) is list:
                for i in self._parameters.get('in-reply-to-user-id'):
                    self.add_attribute('in-reply-to-user-id', value=i)
            else:
                self.add_attribute('in-reply-to-user-id', value=self._parameters['in-reply-to-user-id'])

        # The microblog ID of the microblog this post replies to.
        if self._parameters.get('in-reply-to-status-id'):
            if type(self._parameters.get('in-reply-to-status-id')) is list:
                for i in self._parameters.get('in-reply-to-status-id'):
                    self.add_attribute('in-reply-to-status-id', value=i)
            else:
                self.add_attribute('in-reply-to-status-id', value=self._parameters['in-reply-to-status-id'])

        # The user display name of the microblog this post replies to.
        if self._parameters.get('in-reply-to-display-name'):
            if type(self._parameters.get('in-reply-to-display-name')) is list:
                for i in self._parameters.get('in-reply-to-display-name'):
                    self.add_attribute('in-reply-to-display-name', value=i)
            else:
                self.add_attribute('in-reply-to-display-name', value=self._parameters['in-reply-to-display-name'])

        # The language of the post.
        if self._parameters.get('language'):
            if type(self._parameters.get('language')) is list:
                for i in self._parameters.get('language'):
                    self.add_attribute('language', value=i)
            else:
                self.add_attribute('language', value=self._parameters['language'])

        # Original link into the microblog post (Supposed harmless).
        if self._parameters.get('link'):
            self.add_attribute('link', value=self._parameters['link'])

        # Name of the account that posted this tweet.
        if self._parameters.get('name'):
            self.add_attribute('name', value=self._parameters['name'])

        # If the account contains sensitive content.
        if self._parameters.get('possibly-sensitive'):
            self.add_attribute('possibly-sensitive', value=self._parameters['possibly-sensitive'])

        # Name of the account that posted this tweet.
        if self._parameters.get('possibly-sensitive-appealable'):
            self.add_attribute('possibly-sensitive-appealable',
                               value=self._parameters['possibly-sensitive-appealable'])

        # Raw text posted in this tweet.
        if self._parameters.get('post'):
            self.add_attribute('post', value=self._parameters['post'])

        # Numerical ID of this tweet.
        if self._parameters.get('post-id'):
            self.add_attribute('post-id', value=self._parameters['post-id'])

        # Removal date.
        if self._parameters.get('removal-date'):
            self.add_attribute('removal-date', value=self._parameters['removal-date'])

        # Removal date.
        if self._parameters.get('retweet-count'):
            self.add_attribute('retweet-count', value=self._parameters['retweet-count'])

        # Source device of post.
        if self._parameters.get('source'):
            self.add_attribute('source', value=self._parameters['source'])

        # Original URL location of the microblog post (potentially malicious.
        if self._parameters.get('url'):
            if type(self._parameters.get('url')) is list:
                for i in self._parameters.get('url'):
                    self.add_attribute('url', value=i)
            else:
                self.add_attribute('url', value=self._parameters['url'])

        # ID of account that posted this tweet.
        if self._parameters.get('user-id'):
            self.add_attribute('user-id', value=self._parameters['user-id'])

        # username quoted
        if self._parameters.get('username-quoted'):
            if type(self._parameters.get('username-quoted')) is list:
                for i in self._parameters.get('username-quoted'):
                    self.add_attribute('username-quoted', value=i)
            else:
                self.add_attribute('username-quoted', value=self._parameters['username-quoted'])


class TwitterAccountObject(AbstractMISPObjectGenerator):

    def __init__(self, parameters: dict, strict: bool = True, standalone: bool = True, **kwargs):
        super(TwitterAccountObject, self).__init__('twitter-account', strict=strict, standalone=standalone, **kwargs)
        self._parameters = parameters
        self.generate_attributes()

    def generate_attributes(self):
        # Archive of the original document (Internet Archive, Archive.is, etc).
        if self._parameters.get('archive'):
            if type(self._parameters.get('archive')) is list:
                for i in self._parameters.get('archive'):
                    self.add_attribute('archive', value=i)
            else:
                self.add_attribute('archive', value=self._parameters['archive'])

        # attachment
        if self._parameters.get('attachment'):
            if type(self._parameters.get('attachment')) is list:
                for i in self._parameters.get('attachment'):
                    self.add_attribute('attachment',
                                       value=i["filename"], data=i["data"])
            else:
                self.add_attribute('attachment',
                                   value=self._parameters.get('attachment')["filename"],
                                   data=self._parameters.get('attachment')["data"])

        # biography
        if self._parameters.get('bio'):
            self.add_attribute('bio', value=self._parameters['bio'])

        # description
        if self._parameters.get('description'):
            self.add_attribute('description', value=self._parameters['description'])

        # displayed-name
        if self._parameters.get('displayed-name'):
            self.add_attribute('displayed-name', value=self._parameters['displayed-name'])

        # embedded-link.
        if self._parameters.get('embedded-link'):
            if type(self._parameters.get('embedded-link')) is list:
                for i in self._parameters.get('embedded-link'):
                    self.add_attribute('embedded-link', value=i)
            else:
                self.add_attribute('embedded-link', value=self._parameters['embedded-link'])

        # embedded-safe-link
        if self._parameters.get('embedded-safe-link'):
            if type(self._parameters.get('embedded-safe-link')) is list:
                for i in self._parameters.get('embedded-safe-link'):
                    self.add_attribute('embedded-safe-link', value=i)
            else:
                self.add_attribute('embedded-safe-link', value=self._parameters['embedded-safe-link'])

        # Follower count at time of archive.
        if self._parameters.get('followers'):
            self.add_attribute('followers', value=self._parameters['followers'])

        # Following count at time of archive.
        if self._parameters.get('following'):
            self.add_attribute('following', value=self._parameters['following'])

        # Hashtag into the microblog post.
        if self._parameters.get('hashtag'):
            if type(self._parameters.get('hashtag')) is list:
                for i in self._parameters.get('hashtag'):
                    self.add_attribute('hashtag', value=i)
            else:
                self.add_attribute('hashtag', value=self._parameters['hashtag'])

        # Account ID
        if self._parameters.get('id'):
            self.add_attribute('id', value=self._parameters['id'])

        # Account ID
        if self._parameters.get('likes'):
            self.add_attribute('likes', value=self._parameters['likes'])

        # Original link to the account (Supposed harmless).
        if self._parameters.get('link'):
            self.add_attribute('link', value=self._parameters['link'])

        # Number of lists user is on.
        if self._parameters.get('listed'):
            self.add_attribute('listed', value=self._parameters['listed'])

        # User defined location.
        if self._parameters.get('location'):
            self.add_attribute('location', value=self._parameters['location'])

        # Number of media posts.
        if self._parameters.get('media'):
            self.add_attribute('media', value=self._parameters['media'])

        # Account name without @.
        if self._parameters.get('name'):
            self.add_attribute('name', value=self._parameters['name'])

        # Account name without @.
        if self._parameters.get('private'):
            self.add_attribute('private', value=self._parameters['private'])

        # attachment
        if self._parameters.get('profile-banner'):
            if type(self._parameters.get('profile-banner')) is list:
                for i in self._parameters.get('profile-banner'):
                    self.add_attribute('profile-banner',
                                       value=i["filename"], data=i["data"])
            else:
                self.add_attribute('profile-banner',
                                   value=self._parameters.get('profile-banner')["filename"],
                                   data=self._parameters.get('profile-banner')["data"])

        # link to banner
        if self._parameters.get('profile-banner-url'):
            self.add_attribute('profile-banner-url', value=self._parameters['profile-banner-url'])

        # attachment
        if self._parameters.get('profile-image'):
            if type(self._parameters.get('profile-image')) is list:
                for i in self._parameters.get('profile-image'):
                    self.add_attribute('profile-image',
                                       value=i["filename"], data=i["data"])
            else:
                self.add_attribute('profile-image',
                                   value=self._parameters.get('profile-image')["filename"],
                                   data=self._parameters.get('profile-image')["data"])

        # link to avatar
        if self._parameters.get('profile-image-url'):
            self.add_attribute('profile-image-url', value=self._parameters['profile-image-url'])

        # number of tweets.
        if self._parameters.get('tweets'):
            self.add_attribute('tweets', value=self._parameters['tweets'])

        # verified
        if self._parameters.get('verified'):
            self.add_attribute('verified', value=self._parameters['verified'])

        # Original URL location of the microblog post (potentially malicious.
        if self._parameters.get('url'):
            if type(self._parameters.get('url')) is list:
                for i in self._parameters.get('url'):
                    self.add_attribute('url', value=i)
            else:
                self.add_attribute('url', value=self._parameters['url'])


class MicroblogObject(AbstractMISPObjectGenerator):

    def __init__(self, parameters: dict, strict: bool = True, standalone: bool = True, **kwargs):
        super(MicroblogObject, self).__init__('microblog', strict=strict, standalone=standalone, **kwargs)
        self._parameters = parameters
        self.generate_attributes()

    def generate_attributes(self):
        # Raw post.
        if self._parameters.get('post'):
            self.add_attribute('post', value=self._parameters['post'])

        # Title of the post.
        if self._parameters.get('title'):
            self.add_attribute('title', value=self._parameters['title'])

        # Original link into the microblog post (Supposed harmless).
        if self._parameters.get('link'):
            self.add_attribute('link', value=self._parameters['link'])

        # Original URL location of the microblog post (potentially malicious.
        if self._parameters.get('url'):
            if type(self._parameters.get('url')) is list:
                for i in self._parameters.get('url'):
                    self.add_attribute('url', value=i)
            else:
                self.add_attribute('url', value=self._parameters['url'])

        # Archive of the original document (Internet Archive, Archive.is, etc).
        if self._parameters.get('archive'):
            if type(self._parameters.get('archive')) is list:
                for i in self._parameters.get('archive'):
                    self.add_attribute('archive', value=i)
            else:
                self.add_attribute('archive', value=self._parameters['archive'])

        # Display name of the account who posted the microblog.
        if self._parameters.get('display-name'):
            self.add_attribute('display-name', value=self._parameters['display-name'])

        # The user ID of the microblog this post replies to.
        if self._parameters.get('in-reply-to-user-id'):
            self.add_attribute('in-reply-to-user-id', value=self._parameters['in-reply-to-user-id'])

        # The microblog ID of the microblog this post replies to.
        if self._parameters.get('in-reply-to-status-id'):
            self.add_attribute('in-reply-to-status-id', value=self._parameters['in-reply-to-status-id'])

        # The user display name of the microblog this post replies to.
        if self._parameters.get('in-reply-to-display-name'):
            self.add_attribute('in-reply-to-display-name', value=self._parameters['in-reply-to-display-name'])

        # The language of the post.
        if self._parameters.get('language'):
            self.add_attribute('language', value=self._parameters['language'], disable_correlation=True)

        # TODO: handle attachments
        # The microblog post file or screen capture.
        # if self._parameters.get('attachment'):
        #     self.add_attribute('attachment', value=self._parameters['attachment'])

        # Type of the microblog post.
        type_allowed_values = ["Twitter", "Facebook", "LinkedIn", "Reddit", "Google+",
                               "Instagram", "Forum", "Other"]
        if self._parameters.get('type'):
            if type(self._parameters.get('type')) is list:
                for i in self._parameters.get('type'):
                    if i in type_allowed_values:
                        self.add_attribute('type', value=i)
            else:
                if self._parameters['type'] in type_allowed_values:
                    self.add_attribute('type', value=self._parameters['type'])

        # State of the microblog post.
        type_allowed_values = ["Informative", "Malicious", "Misinformation", "Disinformation", "Unknown"]
        if self._parameters.get('state'):
            if type(self._parameters.get('state')) is list:
                for i in self._parameters.get('state'):
                    if i in type_allowed_values:
                        self.add_attribute('state', value=i)
            else:
                if self._parameters['state'] in type_allowed_values:
                    self.add_attribute('state', value=self._parameters['state'])

        # Username who posted the microblog post (without the @ prefix).
        if self._parameters.get('username'):
            self.add_attribute('username', value=self._parameters['username'])

        # Is the username account verified by the operator of the microblog platform.
        type_allowed_values = ["Verified", "Unverified", "Unknown"]
        if self._parameters.get('verified-username'):
            if type(self._parameters.get('verified-username')) is list:
                for i in self._parameters.get('verified-username'):
                    if i in type_allowed_values:
                        self.add_attribute('verified-username', value=i)
            else:
                if self._parameters['verified-username'] in type_allowed_values:
                    self.add_attribute('verified-username', value=self._parameters['verified-username'])

        # embedded-link.
        if self._parameters.get('embedded-link'):
            if type(self._parameters.get('embedded-link')) is list:
                for i in self._parameters.get('embedded-link'):
                    self.add_attribute('embedded-link', value=i)
            else:
                self.add_attribute('embedded-link', value=self._parameters['embedded-link'])

        # embedded-safe-link
        if self._parameters.get('embedded-safe-link'):
            if type(self._parameters.get('embedded-safe-link')) is list:
                for i in self._parameters.get('embedded-safe-link'):
                    self.add_attribute('embedded-safe-link', value=i)
            else:
                self.add_attribute('embedded-safe-link', value=self._parameters['embedded-safe-link'])

        # Hashtag into the microblog post.
        if self._parameters.get('hashtag'):
            if type(self._parameters.get('hashtag')) is list:
                for i in self._parameters.get('hashtag'):
                    self.add_attribute('hashtag', value=i)
            else:
                self.add_attribute('hashtag', value=self._parameters['hashtag'])

        # username quoted
        if self._parameters.get('username-quoted'):
            if type(self._parameters.get('username-quoted')) is list:
                for i in self._parameters.get('username-quoted'):
                    self.add_attribute('username-quoted', value=i)
            else:
                self.add_attribute('username-quoted', value=self._parameters['username-quoted'])

        # twitter post id
        if self._parameters.get('twitter-id'):
            self.add_attribute('twitter-id', value=self._parameters['twitter-id'])