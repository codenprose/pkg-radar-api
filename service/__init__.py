from flask import Flask
from flask_cors import CORS, cross_origin
import boto3

app = Flask(__name__)
CORS(app)

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

packages_table = db_r.Table('pkg_radar_dev_packages')
package_tags_table = db_r.Table('pkg_radar_dev_package_tags')
package_recommendations_table = db_r.Table('pkd_radar_dev_package_recommendations')
user_kanban_packages_table = db_r.Table('pkg_radar_dev_user_kanban_packages')
user_connections_table = db_r.Table('pkg_radar_dev_user_connections')
users_table = db_r.Table('pkg_radar_dev_users')

from service import views
