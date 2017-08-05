import boto3

session = boto3.Session()
db_r = session.resource('dynamodb')
db_c = session.client('dynamodb')

table_name = ''
owner_name = ''
package_name = ''

query_result = db_r.Table(table_name).get_item(
    Key={
        'owner_name': owner_name,
        'package_name': package_name
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
