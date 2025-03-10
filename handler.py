import json


def hello(event, context):
    body = {
        "message": "Hi, Abhinav Yadav this side."
    }

    return {"statusCode": 200, "body": json.dumps(body)}
