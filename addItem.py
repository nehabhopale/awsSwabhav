import os
import boto3
import json

from boto3.dynamodb.conditions import Key,Attr
dynamodb = boto3.resource('dynamodb')
print(dynamodb)

table_EkartItems=dynamodb.Table('EkartItem')

def lambda_handler(event, context):
    return addItem(event)

def addItem(event):
#POST method- create user
    print("inside register")
    params=json.loads(event['body'])
    print(params['item_id'],params['price'],params['prod_name'],params['quantity_available'],params['supplier_email'])
    
    item_id=params['item_id']
    price=params['price']
    prod_name=params['prod_name']
    quantity_available=params['quantity_available']
    supplier_email=params['supplier_email']
    
    resp= table_EkartItems.get_item(Key={"item_id":item_id})
    print(resp)
    
    if "Item" in resp:
        item_id=resp['Item']['item_id']
        print("Found !! ",item_id)
        return{'statusCode': 200,
        'body': json.dumps('item exists!')}
    
    r=table_EkartItems.put_item(Item={"item_id":item_id,"price":price,"prod_name":prod_name,"quantity_available":quantity_available,"supplier_email":supplier_email})
    return {
    'statusCode': 200,
    'body': json.dumps('item created')
    }