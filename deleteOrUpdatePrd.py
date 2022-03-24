import json
import boto3
from boto3.dynamodb.conditions import Key,Attr
dynamodb = boto3.resource('dynamodb')
print(dynamodb)
table_EkartItems=dynamodb.Table('EkartItem')

def lambda_handler(event, context):
    # TODO implement
    return editProduct(event)

def editProduct(event):
    print(event['httpMethod'])
    if event['httpMethod']=="DELETE":
        params=json.loads(event['body'])
        item_id=params['item_id']
        response = table_EkartItems.delete_item(
            Key={
                'item_id': item_id,
            },
            ConditionExpression="attribute_exists (item_id)",
        )
        return{'statusCode': 200,
        'body': json.dumps('successfully deleted the product')}
        
    if event['httpMethod']=="PUT":
        params=json.loads(event['body'])
        item_id=params['item_id']
        price=params['price']
        prod_name=params["prod_name"]
        quantity_available=params['quantity_available']
        
        response = table_EkartItems.update_item(
            Key={
                'item_id': item_id,
            },
            UpdateExpression="set quantity_available = :quantity_available, price= :price, prod_name= :prod_name",
            ExpressionAttributeValues={
                ':quantity_available': quantity_available,
                ':price': price,
                ':prod_name': prod_name
            },
            ReturnValues="UPDATED_NEW"
        )
        return{'statusCode': 200,
        'body': json.dumps('successfully updated the product')}
        
        