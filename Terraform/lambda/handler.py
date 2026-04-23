import json

def lambda_handler(event, context):
    path = event.get("rawPath", "")

    if path == "/hello":
        body = {"message": "Hello from Terraform Lambda 🚀"}
    elif path == "/profile":
        body = {
            "name": "Philip",
            "role": "Learning AWS + Backend Systems",
            "goal": "Build scalable systems"
        }
    else:
        body = {"error": "Not Found"}

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }
