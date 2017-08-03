import boto3

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

packages_table = db_r.Table('pkg_radar_dev_packages')

query_result = packages_table.get_item(
    Key={
        'owner_name': 'facebook',
        'package_name': 'react'
    },
    ReturnConsumedCapacity='TOTAL'
)

print("Item")
print("-" * 30)
print(query_result['Item'])
print(" ")
print("Consumed Capacity")
print("-" * 30)
print(query_result['ConsumedCapacity'])
