from pymisp.tools.abstractgenerator import AbstractMISPObjectGenerator

class RedditAccount(AbstractMISPObjectGenerator):
    def __init__(self, parameters: dict, strict: bool = True, standalone: bool = True, **kwargs):
        super(RedditAccount, self).__init__('reddit-account', strict=strict, standalone=standalone, **kwargs)
        self._parameters = parameters
        self.generate_attributes()

    def generate_attributes(self):
        #Account avatar
        if self._parameters.get('account-avatar'):
            if type(self._parameters.get('account-avatar')) is list:
                for i in self._parameters.get('account-avatar'):
                    self.add_attribute('account-avatar', value=i)
            else:
                self.add_attribute('account-avatar', value=self._parameters['account-avatar'])

        # Account ID
        if self._parameters.get('account-id'):
            self.add_attribute('account-id', value=self._parameters['account-id'])

        #Account name
        if self._parameters.get('account-name'):
            self.add_attribute('account-name', value=self._parameters['account-name'])

        #Archive
        if self._parameters.get('archive'):
            if type(self._parameters.get('archive')) is list:
                for i in self._parameters.get('archive'):
                    self.add_attribute('archive', value=i)
            else:
                self.add_attribute('archive', self._parameters['archive'])

        #attachment
        if self._parameters.get('attachment'):
            if type(self._parameters.get('attachment')) is list:
                for i in self._parameters.get('attachment'):
                    self.add_attribute('attachment', value=i)
            else:
                self.add_attribute('attachment', self._parameters['attachment'])

        #description
        if self._parameters.get('description'):
            self.add_attribute('description', value=self._parameters['description'])

        #link
        if self._parameters.get('link'):
            self.add_attribute('link', value=self._parameters['link'])

        #moderator-of
        if self._parameters.get('moderator-of'):
            if type(self._parameters.get('moderator-of')) is list:
                for i in self._parameters.get('moderator-of'):
                    self.add_attribute('moderator-of', value=i)
            else:
                self.add_attribute('moderator-of', self._parameters['moderator-of'])

        #trophies
        if self._parameters.get('trophies'):
            if type(self._parameters.get('trophies')) is list:
                for i in self._parameters.get('trophies'):
                    self.add_attribute('trophies', value=i)
            else:
                self.add_attribute('trophies', self._parameters['trophies'])

        #url
        if self._parameters.get('url'):
            self.add_attribute('url', value=self._parameters['url'])

        #user-avatar
        if self._parameters.get('user-avatar'):
            if type(self._parameters.get('user-avatar')) is list:
                for i in self._parameters.get('user-avatar'):
                    self.add_attribute('user-avatar', value=i)
            else:
                self.add_attribute('user-avatar', self._parameters['user-avatar'])

class RedditComment(AbstractMISPObjectGenerator):
    def __init__(self, parameters: dict, strict: bool = True, standalone: bool = True, **kwargs):
        super(RedditComment, self).__init__('reddit-comment', strict=strict, standalone=standalone, **kwargs)
        self._parameters = parameters
        self.generate_attributes()

    def generate_attributes(self):
        #Archive
        if self._parameters.get('archive'):
            if type(self._parameters.get('archive')) is list:
                for i in self._parameters.get('archive'):
                    self.add_attribute('archive', value=i)
            else:
                self.add_attribute('archive', self._parameters['archive'])

        #attachment
        if self._parameters.get('attachment'):
            if type(self._parameters.get('attachment')) is list:
                for i in self._parameters.get('attachment'):
                    self.add_attribute('attachment', value=i)
            else:
                self.add_attribute('attachment', self._parameters['attachment'])

        #comment
        if self._parameters.get('comment'):
            self.add_attribute('comment', value=self._parameters['comment'])

        #creator
        if self._parameters.get('creator'):
            self.add_attribute('creator', value=self._parameters['creator'])

        #description
        if self._parameters.get('description'):
            self.add_attribute('description', value=self._parameters['description'])

        #embedded-link
        if self._parameters.get('embedded-link'):
            if type(self._parameters.get('embedded-link')) is list:
                for i in self._parameters.get('embedded-link'):
                    self.add_attribute('embedded-link', value=i)
            else:
                self.add_attribute('embedded-link', self._parameters['embedded-link'])

        #hashtag
        if self._parameters.get('hashtag'):
            if type(self._parameters.get('hashtag')) is list:
                for i in self._parameters.get('hashtag'):
                    self.add_attribute('hashtag', value=i)
            else:
                self.add_attribute('hashtag', self._parameters['hashtag'])

        #link
        if self._parameters.get('link'):
            self.add_attribute('link', value=self._parameters['link'])

        #subreddit-name
        if self._parameters.get('subreddit-name'):
            if type(self._parameters.get('subreddit-name')) is list:
                for i in self._parameters.get('subreddit-name'):
                    self.add_attribute('subreddit-name', value=i)
            else:
                self.add_attribute('subreddit-name', self._parameters['subreddit-name'])

        #url
        if self._parameters.get('url'):
            self.add_attribute('url', value=self._parameters['url'])

        #username-quoted
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
        #Archive
        if self._parameters.get('archive'):
            if type(self._parameters.get('archive')) is list:
                for i in self._parameters.get('archive'):
                    self.add_attribute('archive', value=i)
            else:
                self.add_attribute('archive', self._parameters['archive'])

        #attachment
        if self._parameters.get('attachment'):
            if type(self._parameters.get('attachment')) is list:
                for i in self._parameters.get('attachment'):
                    self.add_attribute('attachment', value=i)
            else:
                self.add_attribute('attachment', self._parameters['attachment'])

        #comment
        if self._parameters.get('comment'):
            self.add_attribute('comment', value=self._parameters['comment'])

        #creator
        if self._parameters.get('creator'):
            self.add_attribute('creator', value=self._parameters['creator'])

        #description
        if self._parameters.get('description'):
            self.add_attribute('description', value=self._parameters['description'])

        #embedded-link
        if self._parameters.get('embedded-link'):
            if type(self._parameters.get('embedded-link')) is list:
                for i in self._parameters.get('embedded-link'):
                    self.add_attribute('embedded-link', value=i)
            else:
                self.add_attribute('embedded-link', self._parameters['embedded-link'])

        #embedded-safe-link
        if self._parameters.get('embedded-safe-link'):
            if type(self._parameters.get('embedded-safe-link')) is list:
                for i in self._parameters.get('embedded-safe-link'):
                    self.add_attribute('embedded-safe-link', value=i)
            else:
                self.add_attribute('embedded-safe-link', self._parameters['embedded-safe-link'])

        #hashtag
        if self._parameters.get('hashtag'):
            if type(self._parameters.get('hashtag')) is list:
                for i in self._parameters.get('hashtag'):
                    self.add_attribute('hashtag', value=i)
            else:
                self.add_attribute('hashtag', self._parameters['hashtag'])

        #link
        if self._parameters.get('link'):
            self.add_attribute('link', value=self._parameters['link'])

        #post-content
        if self._parameters.get('post-content'):
            self.add_attribute('post-content', value=self._parameters['post-content'])

        #post-title
        if self._parameters.get('post-title'):
            self.add_attribute('post-title', value=self._parameters['post-title'])

        #subreddit-name
        if self._parameters.get('subreddit-name'):
            if type(self._parameters.get('subreddit-name')) is list:
                for i in self._parameters.get('subreddit-name'):
                    self.add_attribute('subreddit-name', value=i)
            else:
                self.add_attribute('subreddit-name', self._parameters['subreddit-name'])

        #url
        if self._parameters.get('url'):
            self.add_attribute('url', value=self._parameters['url'])

        #username-quoted
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
        #Archive
        if self._parameters.get('archive'):
            if type(self._parameters.get('archive')) is list:
                for i in self._parameters.get('archive'):
                    self.add_attribute('archive', value=i)
            else:
                self.add_attribute('archive', self._parameters['archive'])

        #attachment
        if self._parameters.get('attachment'):
            if type(self._parameters.get('attachment')) is list:
                for i in self._parameters.get('attachment'):
                    self.add_attribute('attachment', value=i)
            else:
                self.add_attribute('attachment', self._parameters['attachment'])

        #community-icon
        if self._parameters.get('community-icon'):
            if type(self._parameters.get('community-icon')) is list:
                for i in self._parameters.get('community-icon'):
                    self.add_attribute('community-icon', value=i)
            else:
                self.add_attribute('community-icon', self._parameters['community-icon'])

        #creator
        if self._parameters.get('creator'):
            self.add_attribute('creator', value=self._parameters['creator'])

        #description
        if self._parameters.get('description'):
            self.add_attribute('description', value=self._parameters['description'])

        #embedded-link
        if self._parameters.get('embedded-link'):
            if type(self._parameters.get('embedded-link')) is list:
                for i in self._parameters.get('embedded-link'):
                    self.add_attribute('embedded-link', value=i)
            else:
                self.add_attribute('embedded-link', self._parameters['embedded-link'])

        #embedded-safe-link
        if self._parameters.get('embedded-safe-link'):
            if type(self._parameters.get('embedded-safe-link')) is list:
                for i in self._parameters.get('embedded-safe-link'):
                    self.add_attribute('embedded-safe-link', value=i)
            else:
                self.add_attribute('embedded-safe-link', self._parameters['embedded-safe-link'])

        #hashtag
        if self._parameters.get('hashtag'):
            if type(self._parameters.get('hashtag')) is list:
                for i in self._parameters.get('hashtag'):
                    self.add_attribute('hashtag', value=i)
            else:
                self.add_attribute('hashtag', self._parameters['hashtag'])

        #header-image
        if self._parameters.get('header-image'):
            if type(self._parameters.get('header-image')) is list:
                for i in self._parameters.get('header-image'):
                    self.add_attribute('header-image', value=i)
            else:
                self.add_attribute('header-image', self._parameters['header-image'])
        #link
        if self._parameters.get('link'):
            self.add_attribute('link', value=self._parameters['link'])

        #moderator
        if self._parameters.get('moderator'):
            if type(self._parameters.get('moderator')) is list:
                for i in self._parameters.get('moderator'):
                    self.add_attribute('moderator', value=i)
            else:
                self.add_attribute('moderator', self._parameters['moderator'])

        #privacy
        privacy_allowed = ['Public', 'Private']
        if self._parameters.get('privacy'):
            if self._parameters['privacy'] in privacy_allowed:
                self.add_attribute('privacy', value=self._parameters['privacy'])

        #rules
        if self._parameters.get('rules'):
            self.add_attribute('rules', value=self._parameters['rules'])

        #submit-text
        if self._parameters.get('submit-text'):
            self.add_attribute('submit-text', value=self._parameters['submit-text'])

        #subreddit-alias
        if self._parameters.get('subreddit-alias'):
            if type(self._parameters.get('subreddit-alias')) is list:
                for i in self._parameters.get('subreddit-alias'):
                    self.add_attribute('subreddit-alias', value=i)
            else:
                self.add_attribute('subreddit-alias', self._parameters['subreddit-alias'])

        #subreddit-name
        if self._parameters.get('subreddit-name'):
            self.add_attribute('subreddit-name', value=self._parameters['subreddit-name'])

        #subreddit-type
        if self._parameters.get('subreddit-type'):
            if type(self._parameters.get('subreddit-type')) is list:
                for i in self._parameters.get('subreddit-type'):
                    self.add_attribute('subreddit-type', value=i)
            else:
                self.add_attribute('subreddit-type', self._parameters['subreddit-type'])

        #url
        if self._parameters.get('url'):
            self.add_attribute('url', value=self._parameters['url'])
