import json
import os
import uuid
import tempfile
from datetime import datetime, timezone

import boto3
import pyarrow as pa
import pyarrow.parquet as pq

s3 = boto3.client("s3")

def lambda_handler(event, context):
    bucket = os.environ["DATA_LAKE_BUCKET"]

    rows = []

    for record in event["Records"]:
        message = json.loads(record["body"])

        rows.append({
            "event_type": message.get("event_type"),
            "source": message.get("source"),
            "request_id": message.get("request_id"),
            "event_timestamp": message.get("timestamp")
        })

    if not rows:
        return

    table = pa.Table.from_pylist(rows)

    now = datetime.now(timezone.utc)

    key = (
        f"events_parquet/"
        f"year={now.year}/"
        f"month={now.month:02d}/"
        f"day={now.day:02d}/"
        f"events-{uuid.uuid4()}.parquet"
    )

    with tempfile.NamedTemporaryFile() as tmp:
        pq.write_table(table, tmp.name)
        tmp.seek(0)

        s3.upload_file(tmp.name, bucket, key)

    print(f"Wrote parquet to s3://{bucket}/{key}")