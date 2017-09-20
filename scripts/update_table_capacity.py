import boto3

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

table_name = ''
rcu = 0
wcu = 0

respsonse = db_c.update_table(
    TableName=table_name,
    ProvisionedThroughput={
        'ReadCapacityUnits': rcu,
        'WriteCapacityUnits': wcu
    }
)

print(respsonse)
