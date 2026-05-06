import json
import os
import time
import boto3

sqs = boto3.client("sqs")
dynamodb = boto3.client("dynamodb")

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }

def lambda_handler(event, context):
    path = event.get("rawPath", "")

    if path == "/hello":
        queue_url = os.environ["EVENTS_QUEUE_URL"]

        event_payload = {
            "event_type": "hello_called",
            "source": "api",
            "request_id": context.aws_request_id,
            "timestamp": int(time.time())
        }

        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(event_payload)
        )

        table = os.environ["DYNAMODB_TABLE"]

        dynamodb.update_item(
            TableName=table,
            Key={
                "event_type": {"S": "hello_called"}
            },
            UpdateExpression="ADD #count :inc",
            ExpressionAttributeNames={
                "#count": "count"
            },
            ExpressionAttributeValues={
                ":inc": {"N": "1"}
            }
        )

        return response(200, {
            "message": "Hello from Terraform Lambda 🚀",
            "event_sent": True
        })

    if path == "/profile":
        return response(200, {
            "name": "Philip",
            "role": "Learning AWS + Backend Systems",
            "goal": "Build scalable systems"
        })

    return response(404, {
        "error": "Not Found"
    })