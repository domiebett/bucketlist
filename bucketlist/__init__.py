from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from config import config
from bucketlist.restplus import api
from bucketlist.models import db, User, BucketList, ListItem
from bucketlist.auth.views import ns as auth_ns
from bucketlist.bucketlist.views import ns as bucketlist_ns

def create_app(config_name):

    app = Flask(__name__)
    CORS(app)
    app.url_map.strict_slashes = False
    api.add_namespace(auth_ns)
    api.add_namespace(bucketlist_ns)
    api.init_app(app)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app
