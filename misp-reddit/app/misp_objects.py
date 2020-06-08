from pymisp.tools.abstractgenerator import AbstractMISPObjectGenerator


class RedditAccount(AbstractMISPObjectGenerator):
    def __init__(self, parameters: dict, strict: bool = True, standalone: bool = True, **kwargs):
        super(RedditAccount, self).__init__('reddit-account', strict=strict, standalone=standalone, **kwargs)
        self._parameters = parameters
        self.generate_attributes()

    def generate_attributes(self):
        # Account avatar URL
        if self._parameters.get('account-avatar-url'):
            if type(self._parameters.get('account-avatar-url')) is list:
                for i in self._parameters.get('account-avatar-url'):
                    self.add_attribute('account-avatar-url', value=i)
            else:
                self.add_attribute('account-avatar', value=self._parameters['account-avatar-url'])

        # Account avatar
        if self._parameters.get('account-avatar'):
            if type(self._parameters.get('account-avatar')) is list:
                for i in self._parameters.get('account-avatar'):
                    self.add_attribute('account-avatar', value=i["filename"], data=i["data"])
            else:
                self.add_attribute('account-avatar',
                                   value=self._parameters.get('account-avatar')["filename"],
                                   data=self._parameters.get('account-avatar')["data"])

        # Account ID
        if self._parameters.get('account-id'):
            self.add_attribute('account-id', value=self._parameters['account-id'])

        # Account name
        if self._parameters.get('account-name'):
            self.add_attribute('account-name', value=self._parameters['account-name'])

        # Archive
        if self._parameters.get('archive'):
            if type(self._parameters.get('archive')) is list:
                for i in self._parameters.get('archive'):
                    self.add_attribute('archive', value=i)
            else:
                self.add_attribute('archive', self._parameters['archive'])

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

        # description
        if self._parameters.get('description'):
            self.add_attribute('description', value=self._parameters['description'])

        # link
        if self._parameters.get('link'):
            self.add_attribute('link', value=self._parameters['link'])

        # moderator-of
        if self._parameters.get('moderator-of'):
            if type(self._parameters.get('moderator-of')) is list:
                for i in self._parameters.get('moderator-of'):
                    self.add_attribute('moderator-of', value=i)
            else:
                self.add_attribute('moderator-of', self._parameters['moderator-of'])

        # trophies
        if self._parameters.get('trophies'):
            if type(self._parameters.get('trophies')) is list:
                for i in self._parameters.get('trophies'):
                    self.add_attribute('trophies', value=i)
            else:
                self.add_attribute('trophies', self._parameters['trophies'])

        # url
        if self._parameters.get('url'):
            self.add_attribute('url', value=self._parameters['url'])


class RedditComment(AbstractMISPObjectGenerator):
    def __init__(self, parameters: dict, strict: bool = True, standalone: bool = True, **kwargs):
        super(RedditComment, self).__init__('reddit-comment', strict=strict, standalone=standalone, **kwargs)
        self._parameters = parameters
        self.generate_attributes()

    def generate_attributes(self):
        # Archive
        if self._parameters.get('archive'):
            if type(self._parameters.get('archive')) is list:
                for i in self._parameters.get('archive'):
                    self.add_attribute('archive', value=i)
            else:
                self.add_attribute('archive', self._parameters['archive'])

        # attachment
        if self._parameters.get('attachment'):
            if type(self._parameters.get('attachment')) is list:
                for i in self._parameters.get('attachment'):
                    self.add_attribute('attachment', value=i["filename"], data=i["data"])
            else:
                self.add_attribute('attachment',
                                   value=self._parameters.get('attachment')["filename"],
                                   data=self._parameters.get('attachment')["data"])

        # author
        if self._parameters.get('author'):
            self.add_attribute('author', value=self._parameters['author'])

        # body
        if self._parameters.get('body'):
            self.add_attribute('body', value=self._parameters['body'])

        # description
        if self._parameters.get('description'):
            self.add_attribute('description', value=self._parameters['description'])

        # embedded-link
        if self._parameters.get('embedded-link'):
            if type(self._parameters.get('embedded-link')) is list:
                for i in self._parameters.get('embedded-link'):
                    self.add_attribute('embedded-link', value=i)
            else:
                self.add_attribute('embedded-link', self._parameters['embedded-link'])

        # embedded-safe-link
        if self._parameters.get('embedded-safe-link'):
            if type(self._parameters.get('embedded-safe-link')) is list:
                for i in self._parameters.get('embedded-safe-link'):
                    self.add_attribute('embedded-safe-link', value=i)
            else:
                self.add_attribute('embedded-safe-link', self._parameters['embedded-safe-link'])

        # hashtag
        if self._parameters.get('hashtag'):
            if type(self._parameters.get('hashtag')) is list:
                for i in self._parameters.get('hashtag'):
                    self.add_attribute('hashtag', value=i)
            else:
                self.add_attribute('hashtag', self._parameters['hashtag'])

        # link
        if self._parameters.get('link'):
            self.add_attribute('link', value=self._parameters['link'])

        # link
        if self._parameters.get('subreddit-name'):
            self.add_attribute('subreddit-name', value=self._parameters['subreddit-name'])

        # url
        if self._parameters.get('url'):
            self.add_attribute('url', value=self._parameters['url'])

        # username-quoted
        if self._parameters.get('username-quoted'):
            if type(self._parameters.get('username-quoted')) is list:
                for i in self._parameters.get('username-quoted'):
                    self.add_attribute('username-quoted', value=i)
            else:
                self.add_attribute('username-quoted', self._parameters['username-quoted'])


class RedditPost(AbstractMISPObjectGenerator):
    def __init__(self, parameters: dict, strict: bool = True, standalone: bool = True, **kwargs):
        super(RedditPost, self).__init__('reddit-post', strict=strict, standalone=standalone, **kwargs)
        self._parameters = parameters
        self.generate_attributes()

    def generate_attributes(self):
        # Archive
        if self._parameters.get('archive'):
            if type(self._parameters.get('archive')) is list:
                for i in self._parameters.get('archive'):
                    self.add_attribute('archive', value=i)
            else:
                self.add_attribute('archive', self._parameters['archive'])

        # attachment
        if self._parameters.get('attachment'):
            if type(self._parameters.get('attachment')) is list:
                for i in self._parameters.get('attachment'):
                    self.add_attribute('attachment', value=i["filename"], data=i["data"])
            else:
                self.add_attribute('attachment',
                                   value=self._parameters.get('attachment')["filename"],
                                   data=self._parameters.get('attachment')["data"])

        # comment
        if self._parameters.get('comment'):
            self.add_attribute('comment', value=self._parameters['comment'])

        # author
        if self._parameters.get('author'):
            self.add_attribute('author', value=self._parameters['author'])

        # description
        if self._parameters.get('description'):
            self.add_attribute('description', value=self._parameters['description'])

        # edited
        if self._parameters.get('edited'):
            self.add_attribute('edited', value=self._parameters['edited'])

        # embedded-link
        if self._parameters.get('embedded-link'):
            if type(self._parameters.get('embedded-link')) is list:
                for i in self._parameters.get('embedded-link'):
                    self.add_attribute('embedded-link', value=i)
            else:
                self.add_attribute('embedded-link', self._parameters['embedded-link'])

        # embedded-safe-link
        if self._parameters.get('embedded-safe-link'):
            if type(self._parameters.get('embedded-safe-link')) is list:
                for i in self._parameters.get('embedded-safe-link'):
                    self.add_attribute('embedded-safe-link', value=i)
            else:
                self.add_attribute('embedded-safe-link', self._parameters['embedded-safe-link'])

        # hashtag
        if self._parameters.get('hashtag'):
            if type(self._parameters.get('hashtag')) is list:
                for i in self._parameters.get('hashtag'):
                    self.add_attribute('hashtag', value=i)
            else:
                self.add_attribute('hashtag', self._parameters['hashtag'])

        # link
        if self._parameters.get('link'):
            self.add_attribute('link', value=self._parameters['link'])

        # post-content
        if self._parameters.get('post-content'):
            self.add_attribute('post-content', value=self._parameters['post-content'])

        # post-title
        if self._parameters.get('post-title'):
            self.add_attribute('post-title', value=self._parameters['post-title'])

        # subreddit-name
        if self._parameters.get('subreddit-name'):
            if type(self._parameters.get('subreddit-name')) is list:
                for i in self._parameters.get('subreddit-name'):
                    self.add_attribute('subreddit-name', value=i)
            else:
                self.add_attribute('subreddit-name', self._parameters['subreddit-name'])

        # thumbnail
        if self._parameters.get('thumbnail'):
            self.add_attribute('thumbnail', value=self._parameters.get('thumbnail')["filename"],
                               data=self._parameters.get('thumbnail')["data"])

        # thumbnail-url
        if self._parameters.get('thumbnail-url'):
            self.add_attribute('thumbnail-url', value=self._parameters['thumbnail-url'])

        # url
        if self._parameters.get('url'):
            self.add_attribute('url', value=self._parameters['url'])

        # username-quoted
        if self._parameters.get('username-quoted'):
            if type(self._parameters.get('username-quoted')) is list:
                for i in self._parameters.get('username-quoted'):
                    self.add_attribute('username-quoted', value=i)
            else:
                self.add_attribute('username-quoted', self._parameters['username-quoted'])


class RedditSubReddit(AbstractMISPObjectGenerator):

    def __init__(self, parameters: dict, strict: bool = True, standalone: bool = True, **kwargs):
        super(RedditSubReddit, self).__init__('reddit-subreddit', strict=strict, standalone=standalone, **kwargs)
        self._parameters = parameters
        self.generate_attributes()

    def generate_attributes(self):
        # Archive
        if self._parameters.get('archive'):
            if type(self._parameters.get('archive')) is list:
                for i in self._parameters.get('archive'):
                    self.add_attribute('archive', value=i)
            else:
                self.add_attribute('archive', self._parameters['archive'])

        # attachment
        if self._parameters.get('attachment'):
            if type(self._parameters.get('attachment')) is list:
                for i in self._parameters.get('attachment'):
                    self.add_attribute('attachment', value=i["filename"], data=i["data"])
            else:
                self.add_attribute('attachment',
                                   value=self._parameters.get('attachment')["filename"],
                                   data=self._parameters.get('attachment')["data"])

        # banner-background-image
        if self._parameters.get('banner-background-image'):
            self.add_attribute('banner-background-image',
                               value=self._parameters.get('banner-background-image')["filename"],
                               data=self._parameters.get('banner-background-image')["data"])

        # banner-background-url
        if self._parameters.get('banner-background-url'):
            if type(self._parameters.get('banner-background-url')) is list:
                for i in self._parameters.get('banner-background-url'):
                    self.add_attribute('banner-background-url', value=i)
            else:
                self.add_attribute('banner-background-url', self._parameters['banner-background-url'])

        # creator
        if self._parameters.get('creator'):
            self.add_attribute('creator', value=self._parameters['creator'])

        # description
        if self._parameters.get('description'):
            self.add_attribute('description', value=self._parameters['description'])

        # display-name
        if self._parameters.get('display-name'):
            self.add_attribute('display-name', value=self._parameters['display-name'])

        # embedded-link
        if self._parameters.get('embedded-link'):
            if type(self._parameters.get('embedded-link')) is list:
                for i in self._parameters.get('embedded-link'):
                    self.add_attribute('embedded-link', value=i)
            else:
                self.add_attribute('embedded-link', self._parameters['embedded-link'])

        # embedded-safe-link
        if self._parameters.get('embedded-safe-link'):
            if type(self._parameters.get('embedded-safe-link')) is list:
                for i in self._parameters.get('embedded-safe-link'):
                    self.add_attribute('embedded-safe-link', value=i)
            else:
                self.add_attribute('embedded-safe-link', self._parameters['embedded-safe-link'])

        # hashtag
        if self._parameters.get('hashtag'):
            if type(self._parameters.get('hashtag')) is list:
                for i in self._parameters.get('hashtag'):
                    self.add_attribute('hashtag', value=i)
            else:
                self.add_attribute('hashtag', self._parameters['hashtag'])

        # icon-img
        if self._parameters.get('icon-img'):
            self.add_attribute('icon-img', value=self._parameters.get('icon-img')["filename"],
                               data=self._parameters.get('icon-img')["data"])

        # icon-img-url
        if self._parameters.get('icon-img'):
            self.add_attribute('icon-img', value=self._parameters['icon-img'])

        # link
        if self._parameters.get('link'):
            self.add_attribute('link', value=self._parameters['link'])

        # moderator
        if self._parameters.get('moderator'):
            if type(self._parameters.get('moderator')) is list:
                for i in self._parameters.get('moderator'):
                    self.add_attribute('moderator', value=i)
            else:
                self.add_attribute('moderator', self._parameters['moderator'])

        # privacy
        privacy_allowed = ['Public', 'Private']
        if self._parameters.get('privacy'):
            if self._parameters['privacy'] in privacy_allowed:
                self.add_attribute('privacy', value=self._parameters['privacy'])

        # rules
        if self._parameters.get('rules'):
            if type(self._parameters.get('rules')) is list:
                for i in self._parameters.get('rules'):
                    self.add_attribute('rules', value=i)
            else:
                self.add_attribute('rules', self._parameters['rules'])

        # submit-text
        if self._parameters.get('submit-text'):
            self.add_attribute('submit-text', value=self._parameters['submit-text'])

        # subreddit-alias
        if self._parameters.get('subreddit-alias'):
            if type(self._parameters.get('subreddit-alias')) is list:
                for i in self._parameters.get('subreddit-alias'):
                    self.add_attribute('subreddit-alias', value=i)
            else:
                self.add_attribute('subreddit-alias', self._parameters['subreddit-alias'])

        # subreddit-type
        if self._parameters.get('subreddit-type'):
            if type(self._parameters.get('subreddit-type')) is list:
                for i in self._parameters.get('subreddit-type'):
                    self.add_attribute('subreddit-type', value=i)
            else:
                self.add_attribute('subreddit-type', self._parameters['subreddit-type'])

        # url
        if self._parameters.get('url'):
            self.add_attribute('url', value=self._parameters['url'])
