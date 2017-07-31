import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    APP_NAME = "BucketList"
    SECRET_KEY = os.environ.get("SECRET_KEY") or\
                 "the$weird%key#that@should!not^be&guessed"

class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL")

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "test": TestConfig,
    "default": DevConfig
}
