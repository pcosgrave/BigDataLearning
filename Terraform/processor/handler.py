import json
import os
import time
import uuid
from datetime import datetime, timezone

import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
    bucket = os.environ["DATA_LAKE_BUCKET"]

    for record in event["Records"]:
        body = json.loads(record["body"])

        if "Message" in body:
            message = json.loads(body["Message"])
        else:
            message = body
            
        now = datetime.now(timezone.utc)

        clean_event = {
            "event_type": message.get("event_type"),
            "source": message.get("source"),
            "request_id": message.get("request_id"),
            "event_timestamp": message.get("timestamp"),
            "processed_at": int(time.time())
        }

        key = (
            f"events_clean/"
            f"year={now.year}/"
            f"month={now.month:02d}/"
            f"day={now.day:02d}/"
            f"event-{uuid.uuid4()}.json"
        )

        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(clean_event),
            ContentType="application/json"
        )

        print(f"Wrote clean event to s3://{bucket}/{key}")

    return {"statusCode": 200}