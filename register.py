import json
import os
import boto3
import base64
from boto3.dynamodb.conditions import Key,Attr
dynamodb = boto3.resource('dynamodb')
print(dynamodb)
table_users=dynamodb.Table('Eusers')

print(table_users)

def lambda_handler(event, context):
    print("event-",event)
   
    return registerUser(event)
    
def registerUser(event):
    #POST method- create user
    print("inside register")
    params=json.loads(event['body'])
    print(params['email'],params['fname'],params['lname'],params['pwd'])
    
    email=params['email']
    fname=params['fname']
    lname=params['lname']
    pwd=encodeString(params['pwd'])
    
    resp= table_users.get_item(Key={"email":email})
    print(resp)
    
    if "Item" in resp:
        email=resp['Item']['email']
        print("Found !! ",email)
        return{'statusCode': 200,
        'body': json.dumps('user exists!')}
    
    r=table_users.put_item(Item={"email":email,"fname":fname,"lname":lname,"pwd":pwd})
    return {
    'statusCode': 200,
    'body': json.dumps('user created')
    }
def encodeString(password):
    sample_string = password
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string
  