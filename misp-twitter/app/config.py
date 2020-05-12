import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True

class TestingConfig(Config):
    TESTING = True
