from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Movies')

title = "Kal Ho Na Ho"
year = 2007

response = table.put_item(
   Item={
        'year': year,
        'title': title,
        'info': {
            'plot':"Har Ghadi Badal Rahi Hai.",
            'rating': decimal.Decimal(0)
        }
    }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='Movies')

# Print out some data about the table.
print(table.item_count)
