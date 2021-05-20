#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading

#This function keep listening for a message from the socket
def clientthread(conn, addr):
    # In this while loop, deal with hand-shake
    while True:
        indata = conn.recv(4096).decode("utf-8")
        print('recv: ' + indata[:-1])
        name = indata[11:-1]
        if len(indata) == 0:        # connection closed
            conn.close()
            print('client closed connection.')
            break

        if name in list.keys():     # check if the name is "IN-USE"
            outdata = 'IN-USE\n'
            conn.send(outdata.encode("utf-8"))
        elif len(list) == 65:       # check if connenctions is full (=65), show 'BUSY'
            outdata = 'BUSY\n'
            conn.send(outdata.encode("utf-8"))
        elif ' ' in name:           # check if the name contains ' '
            outdata = 'BAD-RQST-BODY\n'
            conn.send(outdata.encode("utf-8"))
        else:
            list[name] = conn       # add name & conn to dictionary named list
            print(list)
            outdata = 'HELLO ' + name + '\n'
            conn.send(outdata.encode("utf-8"))
            break

    # In this while loop, deal with further actions
    while True:
        indata = conn.recv(4096).decode("utf-8")
        print('recv: ' + indata[:-1])
        if len(indata) == 0:            # connection closed
            del list[name]              # delete the user in the list
            print(list)
            conn.close()
            print('client closed connection.')
            break
        elif indata == 'WHO\n':         # Case: client input '!who'
            outdata = 'WHO-OK '
            for key in list.keys():
                outdata = outdata + key + ','
            outdata = outdata[:-1] + '\n'
            conn.send(outdata.encode("utf-8"))
        elif indata[0:4] == 'SEND':     # Case: client input '@user msg'
            space = indata.find(' ',5)
            if space >= len(indata)-1 or space == -1:   # check if the format is wrong
                outdata = 'BAD-RQST-BODY\n'             # ' ' in last char OR ' ' not found is wrong
                conn.send(outdata.encode("utf-8"))
                continue                                # continue in while loop, let user input again
            user = indata[5:space]
            msg = indata[space+1:-1]
            if user == 'echobot':           # sending msg to echobot
                outdata = 'SEND-OK\n'
                conn.send(outdata.encode("utf-8"))
                outdata = 'DELIVERY echobot ' + msg + '\n'
                conn.send(outdata.encode("utf-8"))
            elif user in list.keys():       # sending msg to other user
                conn2 = list[user]          # copy conn from the list, to coon2
                outdata = 'DELIVERY ' + name + ' ' + msg + '\n'
                conn2.send(outdata.encode("utf-8"))     # send msg to specified user by using conn2.send
                outdata = 'SEND-OK\n'
                conn.send(outdata.encode("utf-8"))
            else:                       # the user is offline
                outdata = 'UNKNOWN\n'
                conn.send(outdata.encode("utf-8"))
                

# server's IP address
HOST = '0.0.0.0'
PORT = 5378
# initialize list of all connected client's sockets, name in the first, conn in second
list = {'echobot':0}

# create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((HOST, PORT))
# listen for upcoming connections, max = 50
s.listen(65)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

while True:
    # keep listening for new connections all the time
    conn, addr = s.accept()
    print('connected by ' + str(addr))
    # start a new thread that listens for each client's messages
    t = threading.Thread(target = clientthread, args = (conn, addr))
    t.setDaemon(True)
    t.start()  
s.close()


