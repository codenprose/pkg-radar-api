import os
from flask import Flask
from flask_cors import CORS, cross_origin
import boto3

app = Flask(__name__)
CORS(app)

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

packages_table = db_r.Table(os.environ.get('packages_table'))
package_tags_table = db_r.Table(os.environ.get('package_tags_table'))
package_recommendations_table = db_r.Table(os.environ.get('package_recommendations_table'))
user_kanban_packages_table = db_r.Table(os.environ.get('user_kanban_packages_table'))
user_connections_table = db_r.Table(os.environ.get('user_connections_table'))
users_table = db_r.Table(os.environ.get('users_table'))

from service import views
