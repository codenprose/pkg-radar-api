import boto3

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

user_kanban_packages_table = db_r.Table('pkg_radar_user_kanban_packages_prod')
username = 'dkh215'

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

    return {
        color=item['color'],
        description=item['description'],
        issues=item['issues'],
        language=item['language'],
        owner_avatar=item['owner_avatar'],
        owner_name=owner_name,
        package_name=package_name,
        stars=item['stars'],
    }

data = user_kanban_packages_table.query(
    ExpressionAttributeValues={':username': username},
    KeyConditionExpression='username = :username',
    ReturnConsumedCapacity='INDEXES'
)

kanban_packages = data['Items']

for item in kanban_packages:
    package_summary_args = {
        'payload': {
            'owner_name': item['owner_name'],
            'package_name': item['package_name']
        }
    }
    # Get package summary data
    package = get_package_summary({}, package_summary_args, {}, info)

    user_kanban_package = {
        'owner_name': package['owner_name'],
        'package_id': package['package_id'],
        'package_name': package['package_name'],
        'status': package['status'],
        'username': kwargs['username']
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
