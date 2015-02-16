#!/usr/bin/env python

"""
Echo Client
"""

import socket


if __name__ == '__main__':
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall("Hey, can you hear me?")
    client_socket.shutdown(socket.SHUT_WR)

    print client_socket.recv(32)
    client_socket.close()
