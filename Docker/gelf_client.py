from pygelf import GelfTcpHandler, GelfUdpHandler, GelfTlsHandler, GelfHttpHandler
import logging
import sys
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.propagate = False

logger.addHandler(GelfUdpHandler(host=os.environ['GELF_LOGGING_HOST'], port=12201))

logger.info(f"Hello from gelf client, logging to {os.environ['GELF_LOGGING_HOST']}")
print(f"Hello from gelf client, logging to {os.environ['GELF_LOGGING_HOST']}")

with open('/sagemaker/gelf_fifo', 'r') as fifo:
    while True:
        for line in fifo:
            logger.info(line)
        time.sleep(1)