import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    APP_NAME = "BucketList"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hiddenkey"

class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/test_bucketlist"

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgressql://localhost/bucketlist_api"

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgressql://localhost/bucketlist_api"


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "test": TestConfig,
    "default": DevConfig
}
