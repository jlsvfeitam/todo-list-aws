import json
import decimalencoder
import todoList


# https://programmingpercy.tech/blog/develop-and-debug-sam/
def translate(event, context):
    # create a response
    item = todoList.get_translate_item(
        event['pathParameters']['id'], event['pathParameters']['language'])
    if item:
        response = {
            "statusCode": 200,
            "body": json.dumps(item,
                               cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response