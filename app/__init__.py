#!/usr/bin/env python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_marshmallow import Marshmallow

# initialization
app = Flask(__name__)

app.config.from_object('app.configuration.ProdConfig')

# extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
from app import models

auth = HTTPBasicAuth()
