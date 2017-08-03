import boto3

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

packages_table = db_r.Table('pkg_radar_dev_packages')

table_name = 'pkg_radar_dev_packages'
index_name = 'package_summary'
rcu = 8
wcu = 8

respsonse = db_c.update_table(
    TableName=table_name,
    GlobalSecondaryIndexUpdates=[
        {
            'Update': {
                'IndexName': index_name,
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': rcu,
                    'WriteCapacityUnits': wcu
                }
            }
        }
    ]
)

print(respsonse)