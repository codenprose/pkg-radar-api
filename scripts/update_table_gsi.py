import boto3

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

table_name = ''
index_name = ''
rcu = 5
wcu = 5

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