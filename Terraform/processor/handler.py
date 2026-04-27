import json

def lambda_handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["body"])
        print("Processing event:", json.dumps(message))

    return {
        "statusCode": 200
    }