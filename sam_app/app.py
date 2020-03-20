import os
import json

def lambda_handler(event, context):
    if 'routeKey' in event:
      str = json.dumps({
            "message": "{} - hello world".format(os.environ["PREFIX"])
        }) 
    else:
      str = '{} - hello world!'.format(os.environ['PREFIX'])
    return str

