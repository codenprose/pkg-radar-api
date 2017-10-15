import os
from flask import Flask
from flask_cors import CORS, cross_origin
import boto3
import logging
from raven import Client
from raven.contrib.flask import Sentry

app = Flask(__name__)
CORS(app)

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

sentry_dsn = os.environ.get('PKG_RADAR_SENTRY_DSN')
clientSentry = Client(sentry_dsn)
sentry = Sentry(app,
                dsn=sentry_dsn,
                logging=True,
                level=logging.ERROR
                )

packages_table = db_r.Table(os.environ.get('packages_table'))
users_table = db_r.Table(os.environ.get('users_table'))
user_connections_table = db_r.Table(os.environ.get('user_connections_table'))
user_kanban_packages_table = db_r.Table(os.environ.get('user_kanban_packages_table'))

from service import views
