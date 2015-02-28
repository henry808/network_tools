#!/usr/bin/env python

"""
Echo Client
"""

import socket
import sys


def echo_client(text):
    """Open a socket and send a string to a server on that socket"""
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall(text)
    client_socket.shutdown(socket.SHUT_WR)
    buffersize = 32
    text_back = ''
    done = False
    while not done:
        msg_part = client_socket.recv(buffersize)
        if len(msg_part) < buffersize:
            done = True
        text_back += msg_part
    client_socket.close()
    return text_back

if __name__ == '__main__':
    try:
        print echo_client(sys.argv[1])
    except:
        raise Exception(u"No message specified. None sent.")