import json
import boto3
import requests
from tqdm import tqdm, trange

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

packages_table = db_r.Table('pkg_radar_packages_prod')

def fetch_pkg(owner, name):
    # print('Fetching {0} / {1}...'.format(owner, name))
    endpoint = 'https://rc5s84uwm4.execute-api.us-east-1.amazonaws.com/dev/service'
    payload = {'owner': owner, 'name': name}

    # fetch github data
    r = requests.post(endpoint, json=payload)
    if r.status_code != requests.codes.ok:
        return r.raise_for_status()

    package = r.json()
    # print('Fetched {0} / {1}'.format(package['owner_name'], package['package_name']))

    return package

def update_package(owner_name, package_name):
    pkg = fetch_pkg(owner_name, package_name)
    # print('Updating {0} / {1}...'.format(pkg['owner_name'], pkg['package_name']))

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

    data = response['Attributes']
    # print('Updated {0} / {1}'.format(data['owner_name'], data['package_name']))

def fetch_packages():
    response = packages_table.scan(
        IndexName='summary-index',
        Select='ALL_PROJECTED_ATTRIBUTES',
        ReturnConsumedCapacity='INDEXES',
        ConsistentRead=True
    )

    packages = tqdm(response['Items'])

    # print('Updating Packages...', len(packages))
    # print('Consumed Capacity', response['ConsumedCapacity']['CapacityUnits'])

    for pkg in packages:
        owner_name = pkg['owner_name']
        package_name = pkg['package_name']
        update_package(owner_name, package_name)

fetch_packages()
