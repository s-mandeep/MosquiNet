import logging

import azure.functions as func
import json
from .detect import tag
def main(req: func.HttpRequest) -> func.HttpResponse:

    image_url = req.params.get('url')
    logging.info('Image URL received: ' + image_url)

    result = tag(image_url)
    res = {
        "image_url":result 
    }
    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    return func.HttpResponse(json.dumps(res), headers = headers)
