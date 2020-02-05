import json
import json
import boto3
from decimal import Decimal
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def getOrderNumber(intent_request):
    flag = 0
    print('intent Request: ', intent_request)
    orderid = intent_request['currentIntent']['slots']['OrderNumber']
    card = int(intent_request['currentIntent']['slots']['CardNumber'])
    order_num = orderid
    table = dynamodb.Table('Order_table')
    response = table.get_item(
                    Key={
                        'OrderId' : orderid}
    )
    
    firstName = response['Item']['FirstName']
    LastName = response['Item']['LastName']
    date = response['Item']['DateOfPurchase']
    product = response['Item']["Product_Desc"]
    card_db =  response['Item']["CardNumber"]
    
    if card==card_db:
        flag = 1
        message = "Hi {} {}! Thank you for confirming your details! Your product is {}".format(firstName,LastName,product)
    else:
        message = "Sorry, your details are incorrect. Please try again later"
    return {
        "dialogAction": {
    "type": "Close",
    "fulfillmentState": "Fulfilled",
    "message": {
      "contentType": "SSML",
      "content": message
    },
    },
    "sessionAttributes": {
    "output": message,
    "orderid" : order_num,
    "name" : firstName,
    "flag" : flag
        }
    }
    
def getReturnDays(intent_request):
    flag = 0
    print('intent Request: ', intent_request)
    orderid = intent_request['currentIntent']['slots']['OrderNumber']
    card = int(intent_request['currentIntent']['slots']['CardNumber'])
    order_num = orderid
    table = dynamodb.Table('Order_table')
    response = table.get_item(
                    Key={
                        'OrderId' : orderid}
    )
    
    returndays = response['Item']['DueDate']
    LastName = response['Item']['LastName']
    date = response['Item']['DateOfPurchase']
    product = response['Item']["Product_Desc"]
    message = "You have {} days more to return your product".format(returndays)

    return {
        "dialogAction": {
    "type": "Close",
    "fulfillmentState": "Fulfilled",
    "message": {
      "contentType": "SSML",
      "content": message
    },
    },
    "sessionAttributes": {
    "output": message,
        }
    }

def dispatch_event(intent_request):
    intent_name = intent_request['currentIntent']['name']
    print('intent_request is : ', intent_request)
    print('intent name is : ', intent_name)
    if intent_name=='OrderNum':
        return getOrderNumber(intent_request)
    elif intent_name == 'vendor_id':
        return getVendorNumber(intent_request)

    


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    return dispatch_event(event)
