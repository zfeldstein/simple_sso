class Config(object):
    """
    Configuration base, for all environments.
    """
    DEBUG = True
    TESTING = False
    DATABASE_URI = 'sqlite:///db3.sqlite'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db3.sqlite'
    BOOTSTRAP_FONTAWESOME = True
    SECRET_KEY = "!f4Sy%rQRO02xGd8#sufeyzAamTgi9*"
    CSRF_ENABLED = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    pass
