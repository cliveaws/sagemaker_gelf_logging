from pygelf import GelfTcpHandler, GelfUdpHandler, GelfTlsHandler, GelfHttpHandler
import logging
import sys
import time
import os




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
#logger.addHandler(GelfTcpHandler(host='127.0.0.1', port=9401))
logger.addHandler(GelfUdpHandler(host=os.environ['GELF_LOGGING_HOST'], port=12201))
#logger.addHandler(GelfTlsHandler(host='127.0.0.1', port=9403))'
#logger.addHandler(GelfHttpHandler(host='127.0.0.1', port=9404))

logger.info(f"Hello from gelf client, logging to {os.environ['GELF_LOGGING_HOST']}")
print(f"Hello from gelf client, logging to {os.environ['GELF_LOGGING_HOST']}")

with open('/sagemaker/gelf_fifo', 'r') as fifo:
    while True:
        for line in fifo:
            logger.info(line)
        time.sleep(1)