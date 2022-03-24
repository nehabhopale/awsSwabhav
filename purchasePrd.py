import json
import os
import boto3
import base64
from boto3.dynamodb.conditions import Key,Attr
dynamodb = boto3.resource('dynamodb')
print(dynamodb)
table_users=dynamodb.Table('Eusers')
table_EkartItems=dynamodb.Table('EkartItem')
table_EkartCart=dynamodb.Table('EkartCart')
print(table_users)

def lambda_handler(event, context):
    # TODO implement
   return buyProduct(event)
    
def buyProduct(event):
    print("welcome to purchase")
    print(event)
    params=json.loads(event['body'])
    print(params['email'],params['item_id'],params['quantity'])
    email=params['email']
    item_id=params['item_id']
    quantity=params['quantity']
    # product=table_EkartItems.scan(FilterExpression=Attr('item_id').eq(item_id))
    product=table_EkartItems.get_item(Key={"item_id":item_id})
    print("[[[",product)

    if "Item" not in product:
        return{'statusCode': 200,
        'body': json.dumps('could not find this product')}
 
    product_price=product['Item']['price']
    product_quantity=product['Item']['quantity_available']
    product_name=product['Item']['prod_name']
    product_supplier_email=product['Item']['supplier_email']
    
    if product_supplier_email==email:
        return{'statusCode': 200,
        'body': json.dumps('could not by ur own product')}
    
    if (product_quantity-quantity)<0:
        return{'statusCode': 200,
        'body': json.dumps('cannot place this order')}
    
    
    resp= table_EkartCart.get_item(Key={"email":email,"item_id":item_id})
    print(resp)
    if "Item" in resp:
        quantityDB=int(resp['Item']['quantity'])
        total_amountDB=int(resp['Item']['total_amount'])
        response = table_EkartCart.update_item(
            Key={
                'item_id': item_id,
                'email':email
            },
            UpdateExpression="set quantity = :quantity, total_amount= :total_amount",
            ExpressionAttributeValues={
                ':quantity': str(quantityDB+int(quantity)),
                ':total_amount': str(total_amountDB+int(quantity)*product_price)
            },
            ReturnValues="UPDATED_NEW"
        )
        
    else:
         a=table_EkartCart.put_item(Item={"item_id":item_id,"email":email,"order_status":"ordered",
        "prod_name":product_name,"quantity":quantity,"total_amount":str(product_price*int(quantity))})
        
    response2 = table_EkartItems.update_item(
        Key={
            'item_id': item_id,
        },
        UpdateExpression="set quantity_available = :quantity_available",
        ExpressionAttributeValues={
            ':quantity_available': str(product_quantity-1),
        },
        ReturnValues="UPDATED_NEW"
    )
    
    return{'statusCode': 200,
    'body': json.dumps('item ordered!')}