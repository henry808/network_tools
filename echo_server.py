#!/usr/bin/env python

"""
Echo Server
"""

import socket

BUFFERSIZE = 32

if __name__ == '__main__':
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)

    try:
        while True:
            response = ''
            done = False
            conn, addr = server_socket.accept()
            while not done:
                msg_part = conn.recv(BUFFERSIZE)
                if len(msg_part) < BUFFERSIZE:
                    done = True
                response += msg_part
            conn.sendall(response)
            conn.close()
    except KeyboardInterrupt:
        pass
    server_socket.close()
