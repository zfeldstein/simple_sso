#!/usr/bin/env python
import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
auth = HTTPBasicAuth()



# initialization
def create_app(conf_file='app.config.ProdConfig'):
    app = Flask(__name__)
    app.config.from_object(conf_file)
    # app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    ma.init_app(app)
    db.init_app(app)

    # from app.views import
    return app

