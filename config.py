import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.urandom(24)
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite: ///" + \
        os.path.join(basedir, "data-dev.sqlite")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite: //"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite: ///" + \
        os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}
