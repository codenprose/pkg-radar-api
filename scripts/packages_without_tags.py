import boto3

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

table_name = 'pkg_radar_packages_prod'

query_result = db_c.scan(
    TableName=table_name,
    ReturnConsumedCapacity='TOTAL'
)

print("-" * 30)
# print(query_result)
# print(" ")
print("Consumed Capacity")
print("-" * 30)
print(query_result['ConsumedCapacity'])
