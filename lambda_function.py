import json, boto3, os, base64
import constants as cnst
from boto3.dynamodb.conditions import Key, Attr
import operator
from functools import reduce

def lambda_handler(event, context):
    
    print(event)
    resource = boto3.resource(cnst.DYNAMODB)
    table = resource.Table(cnst.TABLE_NAME_QA)
    tags = event[cnst.TAGS].split(',')
    image_count = event[cnst.IMAGE_COUNT]
    lastEvaluatedKey = None
    
    if cnst.LAST_EVALUATED_KEY in event:
        lastEvaluatedKey = event[LAST_EVALUATED_KEY]
        
    if image_count > cnst.MAX_IMAGES:
        image_count = cnst.MAX_IMAGES
        
    filterExpression = reduce(operator.or_, (Attr(cnst.TAGS).contains(tag) for tag in tags))

    if not lastEvaluatedKey:
        response = table.scan(
            Limit = image_count,
            FilterExpression = filterExpression,
            ProjectionExpression = cnst.RESPONSE_ATTRIBUTE_LIST,
            ExpressionAttributeNames = cnst.EXPRESSION_ATTRIBUTE_NAMES
        )
    else:
        response = table.scan(
            ExclusiveStartKey = lastEvaluatedKey,
            Limit = image_count,
            FilterExpression = filterExpression,
            ProjectionExpression = cnst.RESPONSE_ATTRIBUTE_LIST,
            ExpressionAttributeNames = cnst.EXPRESSION_ATTRIBUTE_NAMES,
        )
    
    print(response)
    built_response = build_response(response)
    print("API Response: ", built_response)
    return built_response
    
def build_response(scan_response):
    response = { }
    if cnst.LAST_EVALUATED_KEY in scan_response:
        response[cnst.LAST_EVALUATED_KEY] = scan_response[cnst.LAST_EVALUATED_KEY]
    else: 
        response[cnst.LAST_EVALUATED_KEY] = ""          
    response[cnst.ITEMS] = scan_response[cnst.ITEMS]
    return response