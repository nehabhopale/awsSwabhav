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
    # TODO implement
    print("event-",event)
    return loginUser(event)
    
def loginUser(event):
    print("inside login")
    params=json.loads(event['body'])
    print(params['email'],params['pwd'])
    
    email=params['email']
    pwd=encodeString(params['pwd'])
    
    resp= table_users.get_item(Key={"email":email})

    if "Item" in resp:
        print(resp['Item'])
        actualPassword=resp['Item']['pwd']
        if actualPassword==pwd:
            return{'statusCode': 200,
            'body': json.dumps('login succeed!')}
        else:
            return{'statusCode': 200,
            'body': json.dumps('invalid credintials!')}
    return{'statusCode': 200,
        'body': json.dumps('user does not exists!')}
def encodeString(password):
    sample_string = password
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string
  