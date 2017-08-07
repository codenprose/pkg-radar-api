from flask import Flask
import boto3

app = Flask(__name__)

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

packages_table = db_r.Table('pkg_radar_dev_packages')
package_tags_table = db_r.Table('pkg_radar_dev_package_tags')

from service import views