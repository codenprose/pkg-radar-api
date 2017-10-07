import json
import requests
import uuid
from datetime import datetime
import pprint

from service import packages_table, user_kanban_packages_table, \
     users_table, user_connections_table
from .types import Package, UserKanbanPackage, User, UserConnection


# Queries
def get_current_user(root, args, context, info):
    payload = args.get('payload')
    username = payload['username']
    token = payload['token']

    # TODO: validate token
    # client_id = ''
    # client_secret = ''
    #
    # endpoint = 'https://api.github.com/applications/' + client_id + '/tokens/' + token
    # user = requests.get(endpoint, auth=(client_id, client_secret))
    #
    # if user.status_code == 404:
    #     return 'Token not valid'

    data = users_table.get_item(
        Key={
            'username': username
        }
    )

    item = data['Item']

    connections_response = user_connections_table.query(
        ExpressionAttributeValues={':username': username },
        KeyConditionExpression='username = :username',
        ReturnConsumedCapacity='INDEXES'
    )

    connections_data = connections_response['Items']
    connections = []

    if connections_data is not None:
        for connection in connections_data:
            connections.append(
                UserConnection(username=connection['connection'])
            )

    item['connections'] = connections

    print('Retrieved Current User')
    print(item)

    return User(
        id=item['id'],
        avatar=item['avatar'],
        bio=item['bio'] if 'bio' in item else '',
        company=item['company'] if 'company' in item else '',
        connections=item['connections'],
        email=item['email'],
        kanban_boards=item['kanban_boards'] or [],
        kanban_cards=item['kanban_cards'] or [],
        name=item['name'],
        total_subscriptions=item['total_subscriptions'],
        total_packages=item['total_packages'],
        username=item['username'],
        website=item['website'] if 'website' in item else '',
    )


def get_user_connections(root, args, context, info):
    payload = args.get('payload')
    username = payload['username']

    connections_response = user_connections_table.query(
        ExpressionAttributeValues={':username': username },
        KeyConditionExpression='username = :username',
        ReturnConsumedCapacity='INDEXES'
    )

    connections = connections_response['Items']

    response = []
    for connection in connections:
        data = users_table.get_item(
            Key={
                'username': connection['connection']
            }
        )

        item = data['Item']

        response.append(
            UserConnection(
                avatar=item['avatar'],
                bio=item['bio'] if 'bio' in item else '',
                name=item['name'],
                username=item['username']
            )
        )

    return response


def get_user(root, args, context, info):
    payload = args.get('payload')
    username = payload['username']

    data = users_table.get_item(
        Key={
            'username': username
        }
    )

    item = data['Item']

    connections_response = user_connections_table.query(
        ExpressionAttributeValues={':username': username },
        KeyConditionExpression='username = :username',
        ReturnConsumedCapacity='INDEXES'
    )

    connections_data = connections_response['Items']
    connections = []

    for connection in connections_data:
        connections.append(
            UserConnection(username=connection['connection'])
        )

    item['connections'] = connections

    print('Retrieved User')
    print(item['username'])

    return User(
        id=item['id'],
        avatar=item['avatar'],
        bio=item['bio'] if 'bio' in item else '',
        company=item['company'] if 'company' in item else '',
        connections=item['connections'],
        email=item['email'],
        kanban_boards=item['kanban_boards'],
        kanban_cards=item['kanban_cards'],
        name=item['name'],
        total_subscriptions=item['total_subscriptions'],
        total_packages=item['total_packages'],
        username=item['username'],
        website=item['website'] if 'website' in item else '',
    )


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

    print('Retrieved Package')
    print(item['package_name'])

    return Package(
        archive=item['archive'],
        backlog=item['backlog'],
        color=item['color'],
        commits=item['commits'],
        contributors=item['contributors'],
        description=item['description'],
        forks=item['forks'],
        id=item['id'],
        issues=item['issues'],
        language=item['language'],
        last_commit=item['last_commit'],
        last_release=item['last_release'],
        license=item['license'],
        mentionable_users=item['mentionable_users'],
        owner_avatar=item['owner_avatar'],
        owner_name=item['owner_name'],
        package_name=item['package_name'],
        production=item['production'],
        pull_requests=item['pull_requests'],
        readme=item['readme'],
        releases=item['releases'],
        repo_url=item['repo_url'],
        stars=item['stars'],
        tags=item['tags'],
        trial=item['trial'],
        watchers=item['watchers'],
        website_url=item['website_url']
    )


def get_package_summary(root, args, context, info):
    payload = args.get('payload')
    owner_name = payload['owner_name']
    package_name = payload['package_name']

    data = packages_table.query(
        IndexName='summary-index',
        ExpressionAttributeValues={
            ':oname': owner_name, ':pname': package_name},
        KeyConditionExpression='owner_name = :oname AND package_name = :pname',
        ReturnConsumedCapacity='INDEXES'
    )

    item = data['Items'][0]

    print('Retrieved Package Summary')
    print(package_name)

    return Package(
        color=item['color'],
        description=item['description'],
        issues=item['issues'],
        language=item['language'],
        owner_avatar=item['owner_avatar'],
        owner_name=owner_name,
        package_name=package_name,
        stars=item['stars'],
    )


def get_packages(root, args, context, info):
    pkg_filter = args.get('filter')

    if 'language' in pkg_filter:
        data = packages_table.query(
            IndexName='language-index',
            ExpressionAttributeNames={'#L': 'language'},
            ExpressionAttributeValues={':l': pkg_filter['language']},
            KeyConditionExpression='#L = :l',
            ReturnConsumedCapacity='INDEXES'
        )
    # Add more filter cases here

    packages = data['Items']
    response = []

    for item in packages:
        response.append(
            Package(
                color=item['color'],
                description=item['description'],
                issues=item['issues'],
                language=item['language'],
                owner_avatar=item['owner_avatar'],
                owner_name=item['owner_name'],
                package_name=item['package_name'],
                stars=item['stars'],
            )
        )

    return response


def get_user_kanban_packages(root, args, context, info):
    payload = args.get('payload')
    username = payload['username']

    data = user_kanban_packages_table.query(
        ExpressionAttributeValues={':username': username},
        KeyConditionExpression='username = :username',
        ReturnConsumedCapacity='INDEXES'
    )

    kanban_packages = data['Items']
    response = []

    for item in kanban_packages:
        package_summary_args = {
            'payload': {
                'owner_name': item['owner_name'],
                'package_name': item['package_name']
            }
        }
        # Get package summary data
        package = get_package_summary(root, package_summary_args, context, info)

        response.append(
            UserKanbanPackage(
                color=package.color,
                description=package.description,
                issues=package.issues,
                language=package.language,
                owner_avatar=package.owner_avatar,
                owner_name=item['owner_name'],
                package_id=item['package_id'],
                package_name=item['package_name'],
                status=item['status'],
                stars=package.stars,
                username=item['username']
            )
        )

    return response


# Mutations
def create_user(**kwargs):
    # Check if user already exists
    user_exists = users_table.get_item(
        Key={
            'username': kwargs['username']
        }
    )

    if 'Item' in user_exists:
        print('User already exists')
        user_exists_item = user_exists['Item']

        return User(
            avatar=user_exists_item['avatar'],
            bio=user_exists_item['bio'] or '',
            company=user_exists_item['company'] or '',
            created_at=user_exists_item['created_at'],
            email=user_exists_item['email'],
            id=user_exists_item['id'],
            kanban_boards=user_exists_item['kanban_boards'],
            kanban_cards=user_exists_item['kanban_cards'],
            name=user_exists_item['name'],
            total_packages=user_exists_item['total_packages'],
            total_subscriptions=user_exists_item['total_subscriptions'],
            username=user_exists_item['username'],
            website=user_exists_item['website'] or ''
        )

    id = uuid.uuid4()
    date = datetime.isoformat(datetime.now())

    user = {
        'avatar': kwargs['avatar'],
        'created_at': date,
        'email': kwargs['email'],
        'github_id': kwargs['github_id'],
        'id': str(id),
        'kanban_boards': ['All'],
        'kanban_cards': [],
        'name': kwargs['name'],
        'total_packages': 0,
        'total_subscriptions': 0,
        'username': kwargs['username']
    }

    if kwargs['bio']:
        user['bio'] = kwargs['bio']

    if kwargs['website']:
        user['website'] = kwargs['website']

    if kwargs['company']:
        user['company'] = kwargs['company']

    if kwargs['location']:
        user['location']: kwargs['location']

    print('create user')
    print(user)

    item = users_table.put_item(Item=user)

    print('Created user')
    print(item)

    return User(
        avatar=user['avatar'],
        bio=user['bio'] if 'bio' in user else '',
        company=user['company'] if 'company' in user else '',
        created_at=user['created_at'],
        email=user['email'],
        id=user['id'],
        kanban_boards=user['kanban_boards'],
        kanban_cards=user['kanban_cards'],
        name=user['name'],
        total_packages=user['total_packages'],
        total_subscriptions=user['total_subscriptions'],
        username=user['username'],
        website=user['website'] if 'website' in user else ''
    )


def login_user(username, token):
    # validate token

    item = users_table.get_item(
        Key={
            'username': username
        }
    )

    item = data['Item']

    return User(
        avatar=item['avatar'],
        bio=item['bio'] or '',
        company=item['company'] or '',
        email=item['email'],
        id=item['id'],
        kanban_boards=user['kanban_boards'],
        kanban_cards=user['kanban_cards'],
        name=item['name'],
        total_subscriptions=item['total_subscriptions'],
        total_packages=item['total_packages'],
        username=item['username'],
        website=item['website'] or '',
    )


def update_user(**kwargs):
    user = {}
    attributes = {}

    for key in kwargs:
        user[key] = kwargs[key]

        if key != 'username':
            attributes[key] = {
                'Value': user[key],
                'Action': 'PUT'
            }

    item = users_table.update_item(
        Key={ 'username': user['username'] },
        AttributeUpdates=attributes,
        ReturnValues='ALL_OLD'
    )

    data = item['Attributes']

    print('Updated User')
    print(data)

    for key in user:
        if key != 'username':
            data[key] = user[key]

    return User(
        id=data['id'],
        avatar=data['avatar'],
        bio=data['bio'] or '',
        company=data['company'] or '',
        email=data['email'],
        kanban_boards=data['kanban_boards'] or [],
        kanban_cards=data['kanban_cards'] or [],
        name=data['name'],
        total_subscriptions=data['total_subscriptions'],
        total_packages=data['total_packages'],
        username=data['username'],
        website=data['website'] or '',
    )


def create_package(owner, name, created_by):
    endpoint = 'https://rc5s84uwm4.execute-api.us-east-1.amazonaws.com/dev/service'
    payload = {'owner': owner, 'name': name}

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
    package['created_by'] = created_by
    package['id'] = str(id)
    package['production'] = 0
    package['trial'] = 0

    if len(package['tags']) == 0:
        package['tags'].append(package['language'])

    item = packages_table.put_item(
        Item=package,
        ConditionExpression='attribute_not_exists(id)'
    )

    print('Created Package')
    print(package['package_name'])

    return Package(
        archive=package['archive'],
        backlog=package['backlog'],
        color=package['color'],
        commits=package['commits'],
        contributors=package['contributors'],
        created_at=package['created_at'],
        created_by=package['created_by'],
        description=package['description'],
        forks=package['forks'],
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
        releases=package['releases'],
        repo_url=package['repo_url'],
        stars=package['stars'],
        tags=package['tags'],
        trial=package['trial'],
        watchers=package['watchers'],
        website_url=package['website_url']
    )

def update_package(owner, name, data):
    data = json.loads(data)

    print('Update Package', name)
    print('tags', data['tags'])

    response = packages_table.update_item(
        Key={
            'owner_name': owner,
            'package_name': name
        },
        UpdateExpression="set tags = :t",
        ExpressionAttributeValues={
            ':t': data['tags'],
        },
        ReturnValues="ALL_NEW"
    )

    data = response['Attributes']

    print('Update Package Success', data['package_name'])
    print('tags', data['tags'])

    return Package(
        archive=data['archive'],
        backlog=data['backlog'],
        color=data['color'],
        description=data['description'],
        forks=data['forks'],
        id=data['id'],
        issues=data['issues'],
        language=data['language'],
        license=data['license'],
        owner_avatar=data['owner_avatar'],
        owner_name=data['owner_name'],
        package_name=data['package_name'],
        production=data['production'],
        pull_requests=data['pull_requests'],
        repo_url=data['repo_url'],
        stars=data['stars'],
        tags=data['tags'],
        trial=data['trial'],
        watchers=data['watchers'],
        website_url=data['website_url']
    )


def create_user_kanban_package(**kwargs):
    user_kanban_package = {
        'owner_name': kwargs.get('owner_name'),
        'package_id': kwargs.get('package_id'),
        'package_name': kwargs.get('package_name'),
        'status': kwargs.get('status'),
        'username': kwargs.get('username')
    }

    data = user_kanban_packages_table.put_item(Item=user_kanban_package)

    print('Successfully wrote to DynamoDB')
    print(item)

    return UserKanbanPackage(
        owner_name=user_kanban_package['owner_name'],
        package_id=user_kanban_package['package_id'],
        package_name=user_kanban_package['package_name'],
        status=user_kanban_package['status'],
        username=user_kanban_package['username']
    )


def update_user_kanban_package(**kwargs):
    user_kanban_package = {
        'package_id': kwargs.get('package_id'),
        'status': kwargs.get('status'),
        'username': kwargs.get('username')
    }

    item = user_kanban_packages_table.update_item(
        Key={
            'package_id': user_kanban_package['package_id'],
            'username': user_kanban_package['username']
        },
        AttributeUpdates={
            'status': {
                'Value': user_kanban_package['status'],
                'Action': 'PUT'
            }
        },
        ReturnValues='ALL_OLD'
    )

    data = item['Attributes']

    print('Updated Kanban Package Status')
    print(user_kanban_package['status'])

    return UserKanbanPackage(
        owner_name=data['owner_name'],
        package_id=data['package_id'],
        package_name=data['package_name'],
        status=user_kanban_package['status'],
        username=data['username']
    )


def delete_user_kanban_package(**kwargs):
    user_kanban_package = {
        'package_id': kwargs.get('package_id'),
        'username': kwargs.get('username')
    }

    item = user_kanban_packages_table.delete_item(
        Key={
            'package_id': user_kanban_package['package_id'],
            'username': user_kanban_package['username']
        },
        ReturnValues='ALL_OLD'
    )

    data = item['Attributes']

    print('Deleted User Kanban Package')
    print(data)

    return UserKanbanPackage(
        owner_name=data['owner_name'],
        package_id=data['package_id'],
        package_name=data['package_name'],
        status=data['status'],
        username=data['username']
    )


def create_user_connection(**kwargs):
    user_connection = {
        'username': kwargs.get('user'),
        'connection': kwargs.get('connection')
    }

    user_connection_second = {
        'connection': kwargs.get('user'),
        'username': kwargs.get('connection')
    }

    user_connections_table.put_item(Item=user_connection)
    user_connections_table.put_item(Item=user_connection_second)

    print('Created User Connection')
    print(user_connection)

    return UserConnection(username=user_connection['connection'])


def delete_user_connection(**kwargs):
    user_connection = {
        'user': kwargs.get('user'),
        'connection': kwargs.get('connection')
    }

    user_connections_table.delete_item(
        Key={
            'username': user_connection['user'],
            'connection': user_connection['connection']
        }
    )

    user_connections_table.delete_item(
        Key={
            'connection': user_connection['user'],
            'username': user_connection['connection']
        }
    )

    print('Deleted User Connection')
    print(user_connection)

    return UserConnection(username=user_connection['connection'])
