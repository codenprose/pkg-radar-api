import json
import requests
import uuid
from datetime import datetime

from service import packages_table, package_tags_table, package_recommendations_table, \
    user_kanban_packages_table, users_table
from .types import Package, PackageTag, PackageRecommendation, UserKanbanPackage, User


# Queries
def get_current_user(root, args, context, info):
    payload = args.get('payload')
    username = payload['username']
    token = payload['token']

    # # validate token
    # client_id = '1050d5bcb642ab0beb2e'
    # client_secret = 'dacf3ed918494dd629207ff4ebfb05dee261ccc3'
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

    return User(
        id=item['id'],
        avatar=item['avatar'],
        bio=item['bio'] or '',
        company=item['company'] or '',
        website=item['website'] or '',
        name=item['name'],
        username=item['username'],
        email=item['email'],
        total_subscriptions=item['total_subscriptions'],
        total_packages=item['total_packages']
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

    print('-' * 50)
    print('Consumed Capacity: Package')
    print('-' * 50)
    print(data['ConsumedCapacity'])

    tags = get_package_tags(root, { 'payload': { 'package_id': item['id'] }}, context, info)

    return Package(
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
        package_name=item['package_name'],
        production=item['production'],
        pull_requests=item['pull_requests'],
        readme=item['readme'],
        repo_url=item['repo_url'],
        stars=item['stars'],
        tags=tags,
        trial=item['trial'],
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

    print('-' * 50)
    print('Consumed Capacity: Package Summary')
    print('-' * 50)
    print(data['ConsumedCapacity'])

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


def get_package_tags(root, args, context, info):
    payload = args.get('payload')
    package_id = payload['package_id']

    data = package_tags_table.query(
        IndexName='all-tags',
        ExpressionAttributeValues={':id': package_id},
        KeyConditionExpression='package_id = :id',
        ReturnConsumedCapacity='INDEXES'
    )

    tags = data['Items']
    response = []

    for item in tags:
        response.append(
            PackageTag(
                package_id=item['package_id'],
                tag_name=item['tag_name']
            )
        )
    return response


def get_package_recommendations(root, args, context, info):
    payload = args.get('payload')
    package_id = payload['package_id']

    data = package_recommendations_table.query(
        IndexName='all-recommendations',
        ExpressionAttributeValues={':id': package_id},
        KeyConditionExpression='package_id = :id',
        ReturnConsumedCapacity='INDEXES'
    )

    recommendations = data['Items']
    response = []

    # Add get batch item logic
    for item in recommendations:
        response.append(
            PackageRecommendation(
                package_id=item['package_id'],
                recommendation_owner_name=item['recommendation_owner_name'],
                recommendation_package_name=item['recommendation_package_name']
            )
        )

    return response


def get_user_kanban_packages(root, args, context, info):
    payload = args.get('payload')
    user_id = payload['user_id']

    data = user_kanban_packages_table.query(
        IndexName='user-packages-index',
        ExpressionAttributeValues={':user_id': user_id},
        KeyConditionExpression='user_id = :user_id',
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
                board=item['board'],
                color=package.color,
                issues=package.issues,
                language=package.language,
                owner_avatar=package.owner_avatar,
                owner_name=item['owner_name'],
                package_id=item['package_id'],
                package_name=item['package_name'],
                status=item['status'],
                stars=package.stars,
                user_id=item['user_id']
            )
        )

    return response


# Mutations
def create_user(**kwargs):
    id = uuid.uuid4()
    date = datetime.isoformat(datetime.now())

    user = {
        'avatar': kwargs['avatar'],
        'bio': kwargs['bio'],
        'company': kwargs['company'],
        'created_at': date,
        'email': kwargs['email'],
        'github_id': kwargs['github_id'],
        'id': str(id),
        'location': kwargs['location'],
        'name': kwargs['name'],
        'total_packages': 0,
        'total_subscriptions': 0,
        'username': kwargs['username'],
        'website': kwargs['website']
    }

    item = users_table.put_item(Item=user)

    print('Successfully wrote user to DynamoDB')

    return User(
        avatar=user['avatar'],
        bio=user['bio'],
        company=user['company'],
        created_at=user['created_at'],
        email=user['email'],
        id=user['id'],
        name=user['name'],
        total_packages=user['total_packages'],
        total_subscriptions=user['total_subscriptions'],
        username=user['username'],
        website=user['website']
    )


def create_package(owner, name, user):
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


def create_package_tag(tag_name, package_id, owner_name, package_name):
    tag = {
        'tag_name': tag_name,
        'package_id': package_id,
        'owner_name': owner_name,
        'package_name': package_name
    }

    item = package_tags_table.put_item(Item=tag)

    print('Successfully wrote to DynamoDB')
    print(item)

    return PackageTag(
        tag_name=tag['tag_name'],
        package_id=tag['package_id'],
        owner_name=tag['owner_name'],
        package_name=tag['package_name']
    )


def delete_package_tag(package_id, tag_name):
    tag = {
        'package_id': package_id,
        'tag_name': tag_name
    }

    item = package_tags_table.delete_item(
        Key={
            'package_id': package_id,
            'tag_name': tag_name
        }
    )

    print('Successfully wrote to DynamoDB')
    print(item)

    return PackageTag(
        package_id=tag['package_id'],
        tag_name=tag['tag_name']
    )


def create_package_recommendation(**kwargs):
    recommendation = {
        'package_id': kwargs['package_id'],
        'owner_name': kwargs['owner_name'],
        'package_name': kwargs['package_name'],
        'recommendation_package_id': kwargs['recommendation_package_id'],
        'recommendation_owner_name': kwargs['recommendation_owner_name'],
        'recommendation_package_name': kwargs['recommendation_package_name']
    }

    item = package_recommendations_table.put_item(Item=recommendation)

    print('Successfully wrote to DynamoDB')
    print(item)

    return PackageRecommendation(
        package_id=recommendation['package_id'],
        owner_name=recommendation['owner_name'],
        package_name=recommendation['package_name'],
        recommendation_package_id=recommendation['recommendation_package_id'],
        recommendation_owner_name=recommendation['recommendation_owner_name'],
        recommendation_package_name=recommendation['recommendation_package_name']
    )


def delete_package_recommendation(**kwargs):
    recommendation = {
        'package_id': kwargs['package_id'],
        'recommendation_package_id': kwargs['recommendation_package_id'],
        'recommendation_owner_name': kwargs['recommendation_owner_name'],
        'recommendation_package_name': kwargs['recommendation_package_name']
    }

    item = package_recommendations_table.delete_item(
        Key={
            'package_id': recommendation['package_id'],
            'recommendation_package_id': recommendation['recommendation_package_id']
        }
    )

    print('Successfully wrote to DynamoDB')
    print(item)

    return PackageRecommendation(
        package_id=recommendation['package_id'],
        recommendation_package_id=recommendation['recommendation_package_id'],
        recommendation_owner_name=recommendation['recommendation_owner_name'],
        recommendation_package_name=recommendation['recommendation_package_name']
    )


def create_user_kanban_package(**kwargs):
    user_kanban_package = {
        'board': kwargs.get('board'),
        'owner_name': kwargs.get('owner_name'),
        'package_id': kwargs.get('package_id'),
        'package_name': kwargs.get('package_name'),
        'status': kwargs.get('status'),
        'user_id': kwargs.get('user_id')
    }

    item = user_kanban_packages_table.put_item(Item=user_kanban_package)

    print('Successfully wrote to DynamoDB')
    print(item)

    return UserKanbanPackage(
        board=user_kanban_package['board'],
        owner_name=user_kanban_package['owner_name'],
        package_id=user_kanban_package['package_id'],
        package_name=user_kanban_package['package_name'],
        status=user_kanban_package['status'],
        user_id=user_kanban_package['user_id']
    )


def update_user_kanban_package(**kwargs):
    user_kanban_package = {
        'board': kwargs.get('board'),
        'owner_name': kwargs.get('owner_name'),
        'package_id': kwargs.get('package_id'),
        'package_name': kwargs.get('package_name'),
        'status': kwargs.get('status'),
        'user_id': kwargs.get('user_id')
    }

    item = user_kanban_packages_table.update_item(
        Key={
            'package_id': user_kanban_package['package_id'],
            'user_id': user_kanban_package['user_id']
        },
        AttributeUpdates={
            'status': {
                'Value': user_kanban_package['status'],
                'Action': 'PUT'
            },
            'board': {
                'Value': user_kanban_package['board'],
                'Action': 'PUT'
            }
        },
        ReturnValues='ALL_NEW'
    )

    print('Successfully wrote to DynamoDB')
    print(item)

    return UserKanbanPackage(
        board=user_kanban_package['board'],
        owner_name=user_kanban_package['owner_name'],
        package_id=user_kanban_package['package_id'],
        package_name=user_kanban_package['package_name'],
        status=user_kanban_package['status'],
        user_id=user_kanban_package['user_id']
    )


def delete_user_kanban_package(**kwargs):
    user_kanban_package = {
        'board': kwargs.get('board'),
        'owner_name': kwargs.get('owner_name'),
        'package_id': kwargs.get('package_id'),
        'package_name': kwargs.get('package_name'),
        'status': kwargs.get('status'),
        'user_id': kwargs.get('user_id')
    }

    item = user_kanban_packages_table.delete_item(
        Key={
            'package_id': user_kanban_package['package_id'],
            'user_id': user_kanban_package['user_id']
        }
    )

    print('Successfully wrote to DynamoDB')
    print(item)

    return UserKanbanPackage(
        board=user_kanban_package['board'],
        owner_name=user_kanban_package['owner_name'],
        package_id=user_kanban_package['package_id'],
        package_name=user_kanban_package['package_name'],
        status=user_kanban_package['status'],
        user_id=user_kanban_package['user_id']
    )
