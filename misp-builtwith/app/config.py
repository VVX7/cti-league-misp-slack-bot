import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

# Only production config should be used in production.
class ProductionConfig(Config):
    DEBUG = False

# This is not safe. Don't do this.
class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True

# This is not safe. Don't do this either.
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True

# Nope.
class TestingConfig(Config):
    TESTING = True
