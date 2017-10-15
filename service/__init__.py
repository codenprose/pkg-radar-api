import os
import json
import requests
from flask import Flask
from flask_cors import CORS, cross_origin
import boto3
import logging
from raven import Client
from raven.contrib.flask import Sentry
from zappa.async import task

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

@task
def update_package(owner_name, package_name):
    try:
        endpoint = 'https://rc5s84uwm4.execute-api.us-east-1.amazonaws.com/dev/service'
        payload = {'owner': owner_name, 'name': package_name}

        # fetch github data
        r = requests.post(endpoint, json=payload)
        if r.status_code != requests.codes.ok:
            return r.raise_for_status()

        pkg = r.json()

        # update item in dynamodb
        response = packages_table.update_item(
            Key={
                'owner_name': pkg['owner_name'],
                'package_name': pkg['package_name']
            },
            AttributeUpdates={
                'commits': {
                    'Value': pkg['commits'],
                    'Action': 'PUT'
                },
                'contributors': {
                    'Value': pkg['contributors'],
                    'Action': 'PUT'
                },
                'description': {
                    'Value': pkg['description'],
                    'Action': 'PUT'
                },
                'forks': {
                    'Value': pkg['forks'],
                    'Action': 'PUT'
                },
                'issues': {
                    'Value': pkg['issues'],
                    'Action': 'PUT'
                },
                'language': {
                    'Value': pkg['language'],
                    'Action': 'PUT'
                },
                'last_commit': {
                    'Value': pkg['last_commit'],
                    'Action': 'PUT'
                },
                # 'last_release': {
                #     'Value': pkg['last_release'],
                #     'Action': 'PUT'
                # },
                'license': {
                    'Value': pkg['license'],
                    'Action': 'PUT'
                },
                'mentionable_users': {
                    'Value': pkg['mentionable_users'],
                    'Action': 'PUT'
                },
                'owner_avatar': {
                    'Value': pkg['owner_avatar'],
                    'Action': 'PUT'
                },
                'readme': {
                    'Value': pkg['readme'],
                    'Action': 'PUT'
                },
                'releases': {
                    'Value': pkg['releases'],
                    'Action': 'PUT'
                },
                'stars': {
                    'Value': pkg['stars'],
                    'Action': 'PUT'
                },
                'watchers': {
                    'Value': pkg['watchers'],
                    'Action': 'PUT'
                },
                'website_url': {
                    'Value': pkg['website_url'],
                    'Action': 'PUT'
                }
            },
            ReturnValues="ALL_NEW"
        )
    except Exception:
        clientSentry.captureException()

def fetch_packages():
    response = packages_table.scan(
        IndexName='summary-index',
        Select='ALL_PROJECTED_ATTRIBUTES',
        ReturnConsumedCapacity='INDEXES',
        ConsistentRead=True
    )

    packages = response['Items']

    for pkg in packages:
        owner_name = pkg['owner_name']
        package_name = pkg['package_name']

        update_package(owner_name, package_name)
