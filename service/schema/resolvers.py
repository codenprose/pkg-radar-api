import json
import requests
import uuid
from datetime import datetime

from service import packages_table
from .types import Package


def get_package(root, args, context, info):
    payload = args.get('payload')
    owner_name = payload['owner_name']
    package_name = payload['package_name']

    data = packages_table.get_item(
        Key={
            'owner_name': owner_name,
            'package_name': package_name
        },
        ReturnConsumedCapacity='TOTAL'
    )

    item = data['Item']

    response = Package(
        archive=item['archive'],
        backlog=item['backlog'],
        color=item['color'],
        description=item['description'],
        id=item['id'],
        issues=item['issues'],
        language=item['language'],
        last_commit=item['last_commit'],
        last_release=item['last_release'],
        license=item['license'],
        mentionable_users=item['mentionable_users'],
        owner_avatar=item['owner_avatar'],
        owner_name=item['owner_name'],
        package_avatar=item['package_avatar'],
        package_name=item['package_name'],
        production=item['production'],
        pull_requests=item['pull_requests'],
        readme=item['readme'],
        repo_url=item['repo_url'],
        stars=item['stars'],
        trial=item['trial'],
        website_url=item['website_url']
    )
    
    print('-' * 50)
    print('Consumed Capacity: Package')
    print('-' * 50)
    print(data['ConsumedCapacity'])

    return response


def get_package_summary(root, args, context, info):
    payload = args.get('payload')
    owner_name = payload['owner_name']
    package_name = payload['package_name']

    data = packages_table.query(
        IndexName='package_summary',
        ExpressionAttributeValues={':oname': owner_name,':pname': package_name},
        KeyConditionExpression='owner_name = :oname AND package_name = :pname',
        ReturnConsumedCapacity='INDEXES'
    )

    item = data['Items'][0]
    
    package_avatar = ''
    if 'package_avatar' in item:
        package_avatar = item['package_avatar']

    response = Package(
        archive=item['archive'],
        backlog=item['backlog'],
        color=item['color'],
        description=item['description'],
        issues=item['issues'],
        language=item['language'],
        owner_avatar=item['owner_avatar'],
        owner_name=item['owner_name'],
        package_avatar=package_avatar,
        package_name=item['package_name'],
        production=item['production'],
        stars=item['stars'],
        trial=item['trial'],
    )
    print('-' * 50)
    print('Consumed Capacity: Package Summary')
    print('-' * 50)
    print(data['ConsumedCapacity'])

    return response


def create_package(owner, name, user):
    endpoint = 'https://rc5s84uwm4.execute-api.us-east-1.amazonaws.com/dev/service'
    payload = { 'owner': owner, 'name': name }
    
    # fetch github data
    r = requests.post(endpoint, json=payload)
    if r.status_code != requests.codes.ok:
        return r.raise_for_status()

    package = r.json()

    id = uuid.uuid4()
    date = datetime.isoformat(datetime.now())

    package['archive'] = 0
    package['backlog'] = 0
    package['created_at'] = date
    package['created_by'] = user
    package['id'] = str(id)
    package['production'] = 0
    package['trial'] = 0

    item = packages_table.put_item(Item=package)

    print('Successfully wrote to DynamoDB')
    print(item)

    return Package(
        archive=package['archive'],
        backlog=package['backlog'],
        color=package['color'],
        created_at=package['created_at'],
        created_by=package['created_by'],
        description=package['description'],
        id=package['id'],
        issues=package['issues'],
        language=package['language'],
        last_commit=package['last_commit'],
        last_release=package['last_release'],
        license=package['license'],
        mentionable_users=package['mentionable_users'],
        owner_avatar=package['owner_avatar'],
        owner_name=package['owner_name'],
        package_name=package['package_name'],
        production=package['production'],
        pull_requests=package['pull_requests'],
        readme=package['readme'],
        repo_url=package['repo_url'],
        stars=package['stars'],
        trial=package['trial'],
        website_url=package['website_url']
    )
