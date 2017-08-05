from service import packages_table
from .queries import Package


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
