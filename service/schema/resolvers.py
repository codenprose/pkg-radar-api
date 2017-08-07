import json
import requests
import uuid
from datetime import datetime

from service import packages_table, package_tags_table, package_recommendations_table, \
    user_kanban_packages_table
from .types import Package, PackageTag, PackageRecommendation, UserKanbanPackage


# Queries
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
        trial=item['trial'],
        website_url=item['website_url']
    )


def get_package_summary(root, args, context, info):
    payload = args.get('payload')
    owner_name = payload['owner_name']
    package_name = payload['package_name']

    data = packages_table.query(
        IndexName='summary_index',
        ExpressionAttributeValues={':oname': owner_name,':pname': package_name},
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
            ExpressionAttributeNames={ '#L': 'language' },
            ExpressionAttributeValues={ ':l': pkg_filter['language'] },
            KeyConditionExpression='#L = :l',
            ReturnConsumedCapacity='INDEXES'
        )

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
                recommendation_owner_name = item['recommendation_owner_name'],
                recommendation_package_name = item['recommendation_package_name']
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
        response.append(
            UserKanbanPackage(
                board=item['board'],
                owner_name=item['owner_name'],
                package_id=item['package_id'],
                package_name=item['package_name'],
                status=item['status'],
                user_id=item['user_id']
            )
        )
    
    return response


# Mutations
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