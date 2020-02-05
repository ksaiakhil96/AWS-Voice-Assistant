import json
import boto3
from decimal import Decimal
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
def lambda_handler(event, context):
    dict_final = {}
    bucket = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    
    json_object = s3_client.get_object(Bucket = bucket, Key = filename)
    jsonFileReader = json_object['Body'].read()
    json_dict = json.loads(jsonFileReader)
    table = dynamodb.Table('Order_table')
    print(json_dict)
    
    with table.batch_writer() as batch:
        for temp_dict in json_dict:
            for key, value in temp_dict.items():
               
                dict_final[key] = value
                
            table.put_item(Item = dict_final)
        

