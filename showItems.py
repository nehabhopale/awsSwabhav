import json
import os
import boto3
import decimal
from boto3.dynamodb.conditions import Key,Attr
dynamodb = boto3.resource('dynamodb')
print(dynamodb)
table_users=dynamodb.Table('Eusers')
table_EkartItems=dynamodb.Table('EkartItem')

print(table_users)
def lambda_handler(event, context):
    print(event)
    if event['resource']=="/getallproducts":
        return showAllProducts(event)
    if event['resource']=="/getmyproducts":
        return showMyProducts(event)



class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)
def showMyProducts(event):
    #GET method-show user created products
    print(event)
    params=event['queryStringParameters']
    print(params['email'])
    email=params['email']
    resp=table_EkartItems.scan(FilterExpression=Attr('supplier_email').eq(email))
    print("Query ",resp['Items'])

    if "Items" in resp:
        return{'statusCode': 200,
        'body': json.dumps(resp["Items"], cls=DecimalEncoder)}

    return {
        'statusCode': 200,
        'body': json.dumps('no items available')
    }  
def showAllProducts(event):
    #GET method-show all products except user created products
    print(event)
    params=event['queryStringParameters']
    print(params['email'])
    email=params['email']
    resp=table_EkartItems.scan(FilterExpression=Attr('supplier_email').ne(email))
    print("Query ",resp['Items'])

    if "Items" in resp:
        return{'statusCode': 200,
        'body': json.dumps(resp["Items"], cls=DecimalEncoder)}

    return {
        'statusCode': 200,
        'body': json.dumps('no items available')
    }
