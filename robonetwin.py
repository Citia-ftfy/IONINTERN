#
#   Modified Hello World code
#

import zmq
import base64
import argparse
import time
import array

parser = argparse.ArgumentParser()

parser.add_argument('-img','--images', type=str, nargs='*')
args = parser.parse_args()

images = args.images

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://172.19.52.125:8080")

for image in images:
    f = open(image,'rb')
    bytes = bytearray(f.read())
    strng = base64.b64encode(bytes)
    bts = image.encode('utf-8')
    socket.send_multipart([bts,strng])
    f.close()

#  Get the reply.
#message = socket.recv()
#print(f"Received reply {request} [ {message} ]")

#  Do 10 requests, waiting each time for a response
