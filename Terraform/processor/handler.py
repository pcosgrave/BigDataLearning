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
        message = json.loads(record["body"])

        now = datetime.now(timezone.utc)

        key = (
            f"events/"
            f"year={now.year}/"
            f"month={now.month:02d}/"
            f"day={now.day:02d}/"
            f"event-{uuid.uuid4()}.json"
        )

        output = {
            "processed_at": int(time.time()),
            "raw_event": message
        }

        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(output),
            ContentType="application/json"
        )

        print(f"Wrote event to s3://{bucket}/{key}")

    return {
        "statusCode": 200
    }