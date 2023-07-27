#
# Modified Hello World Sending code
#
import base64
import time
import zmq
import cv2


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:8080")

while True:
    #  Wait for next request from client
    message = socket.recv_multipart()
    f = open(message[0].decode('utf-8'), 'wb')
    ba = bytearray(base64.b64decode(message[1]))
    f.write(ba)
    f.close()
    img = cv2.imread(message[0].decode('utf-8'))
    b,g,r = cv2.split(img)
    b = cv2.bitwise_not(b)
    g = cv2.bitwise_not(g)
    r = cv2.bitwise_not(r)
    cv2.imwrite("blue_"+message[0].decode('utf-8'), b)
    cv2.imwrite("green_"+message[0].decode('utf-8'), g)
    cv2.imwrite("red_"+message[0].decode('utf-8'), r)
    print(f"Received request: {message}")

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"Received")
    
#TODO SWITCH THE DIRECTION OF ALL THIS

#LINE 2940 of the processing file is the key, lets remake this in either java or python