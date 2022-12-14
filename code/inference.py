import json
import requests

from pygelf import GelfTcpHandler, GelfUdpHandler, GelfTlsHandler, GelfHttpHandler
import logging
import os
import subprocess


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
#logger.addHandler(GelfTcpHandler(host='127.0.0.1', port=9401))
logger.addHandler(GelfUdpHandler(host=os.environ['GELF_LOGGING_HOST'], port=12201))
#logger.addHandler(GelfTlsHandler(host='127.0.0.1', port=9403))
#logger.addHandler(GelfHttpHandler(host='127.0.0.1', port=9404))



def handler(data, context, res=None):
    """Handle request.
    Args:
        data (obj): the request data
        context (Context): an object containing request and configuration details
    Returns:
        (bytes, string): data to return to client, (optional) response content type
    """
    if res != None:
        #unpack our custom attributes
        custom_attrib = json.loads(context.custom_attributes)


        processed_input = _process_input(data, context)
        response = requests.post(context.rest_uri, data=processed_input)

        # Update our custom attributes and add a new field
        custom_attrib['content'] = 'This is some new content'
        custom_attrib['new_field'] = 'this is a new field'
        res.append_header('X-AMZN-SAGEMAKER-CUSTOM-ATTRIBUTES',json.dumps(custom_attrib))

    body, content_type = _process_output(response, context)

    return body, content_type

def _process_input(data, context):
    if context.request_content_type == 'application/json':
        # pass through json (assumes it's correctly formed)
        d = data.read().decode('utf-8')
        return d if len(d) else ''

    if context.request_content_type == 'text/csv':
        # very simple csv handler
        return json.dumps({
            'instances': [float(x) for x in data.read().decode('utf-8').split(',')]
        })

    raise ValueError('{{"error": "unsupported content type {}"}}'.format(
        context.request_content_type or "unknown"))


def _process_output(data, context):
    
    if data.status_code != 200:
        raise ValueError(data.content.decode('utf-8'))

    response_content_type = context.accept_header
    prediction = data.content
    logging.info(f'{prediction}')
    return prediction, response_content_type 

