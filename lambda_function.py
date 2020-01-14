import json, boto3, os, base64
import constants as cnst
from boto3.dynamodb.conditions import Key, Attr
import operator
from functools import reduce

def lambda_handler(event, context):
    
    print(event)
    resource = boto3.resource('dynamodb')
    table = resource.Table(cnst.TABLE_NAME_QA)
    tags = event['tags'].split(',')
    image_count = event['image_count']
    lastEvaluatedKey = None
    
    if 'LastEvaluatedKey' in event:
        lastEvaluatedKey = event['lastEvaluatedKey']
        
    if image_count > cnst.MAX_IMAGES:
        image_count = cnst.MAX_IMAGES
        
    filterExpression = reduce(operator.or_, (Attr('tags').contains(tag) for tag in tags))

    if not lastEvaluatedKey:
        response = table.scan(
            Limit = image_count,
            FilterExpression = filterExpression
        )
    else:
        response = table.scan(
            ExclusiveStartKey = lastEvaluatedKey,
            Limit = image_count,
            FilterExpression = filterExpression
        )
    
    print(response)
    return response['Items']