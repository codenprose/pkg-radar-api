import boto3

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

table_name = 'pkg_radar_packages_prod'
rcu = 100
wcu = 20

respsonse = db_c.update_table(
    TableName=table_name,
    ProvisionedThroughput={
        'ReadCapacityUnits': rcu,
        'WriteCapacityUnits': wcu
    }
)

print(respsonse)
