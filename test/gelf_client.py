#!/usr/bin/env python

############### // gelfListener 0.2 // ###############
#
# Listens on UDP 12201 for Gelf messages
# Extracts the event data and writes the message to disk
# updated to handle both zlib (nxlog) and gzip (graylog server) compressed events
# not perfect, but works okay
#
# Bugs:
#
# decodeGzip() blows up a lot. Take out the try: finally to see all
# the pretty error messages
#
######################################################

import gzip
import zlib
import json
import socket
from io import StringIO
import sys
from datetime import datetime

HOST = 'ec2-54-171-198-20.eu-west-1.compute.amazonaws.com'   # Symbolic name meaning all available interfaces
PORT = 12201 # Default port for Gelf UDP

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # this creates UDP socket
print("Socket created")

#Bind socket to local host and port
try:
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    #s.setblocking(0)
except socket.error as msg:
    print('Bind failed. Error Code : ' + ' Message ' + str(msg))
    sys.exit()

print('Socket bind complete')


############### // fileWriter // ###############

def fileWriter(myHostName, myMessage):
    with open(myHostName, 'a') as fileWriteOperation:
        fileWriteOperation.write(myMessage + '\n')
        fileWriteOperation.close()

################################################

############### // Zlib // ###############

def decodeZlib(zData):
    # decompress
    event = zlib.decompress(zData)
    parsed_json = json.loads(event)

    # assign
    #print(parsed_json)
    hostname = parsed_json["host"]
    #fullMessage = parsed_json["full_message"]
    shortMessage = parsed_json["short_message"]
    time = datetime.fromtimestamp(parsed_json['timestamp'])
    # output
    fileWriter(hostname, shortMessage)
    print(f'{time.isoformat()} {hostname} {shortMessage}')

##########################################


############### // Gzip // ###############

def decodeGzip(gData):
    try:
        # decompress
        gzipEvent = StringIO(gData.encode( 'utf-8'))
        gzipper = gzip.GzipFile(fileobj=gzipEvent)
        extractedData = gzipper.read()
        parsed_json = json.loads(extractedData)

        # assign
        print(parsed_json)
        hostname = str(parsed_json["host"])
        #fullMessage = parsed_json["full_message"]
        shortMessage = parsed_json["short_message"]

        # output
        fileWriter(hostname, shortMessage)
        print(hostname, parsed_json)

        # exception handling
    except:
        pass
##########################################


############### // Here's the Magic // ###############
print("reading stream now")
while True:
    # 8192 is the largest size that a udp packet can handle
    data, addr = s.recvfrom(8192) # buffer size is 8192 bytes
    try:
        decodeZlib(data)
    except Exception as e:
        print(e)
        decodeGzip(data)
