#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading
import time

def receive_message():
    while not stopThread:
        indata = s.recv(4096).decode("utf-8")
        if len(indata) == 0: # connection closed
            s.close()
            print('server closed connection.')
            break
        print(indata[:-1])
        time.sleep(0.25)


HOST = '192.168.50.209'  #0.0.0.0'      # 3.121.226.198
PORT = 5378
# initialize TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    outdata = input('please input name: ')
    outdata = 'HELLO-FROM ' + outdata + '\n'
    s.send(outdata.encode("utf-8"))
    
    indata = s.recv(4096).decode("utf-8")
    if len(indata) == 0: # connection closed
        s.close()
        print('server closed connection.')
        break
    print(indata[:-1])
    if indata != 'IN-USE\n' and indata != 'BUSY\n' and indata != 'BAD-RQST-HDR\n' and indata != 'BAD-RQST-BODY\n':
        break

t = threading.Thread(target=receive_message)
t.setDaemon(True)
stopThread = False
t.start()  

while True:
    outdata = input('please input action: ')
    if outdata == '':
        continue
    if outdata == '!quit':
        stopThread = True
        time.sleep(1)
        s.close()
        print('close socket')
        break
    elif outdata == '!who':
        outdata = 'WHO\n'
        s.send(outdata.encode("utf-8"))
    elif '@' in outdata:
        space = outdata.find(' ')
        user = outdata[1:space]
        msg = outdata[space+1:]
        outdata = 'SEND ' + user + ' ' + msg + '\n'
        s.send(outdata.encode("utf-8"))
    else:
        pass
    time.sleep(1)

