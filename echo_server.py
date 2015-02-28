#!/usr/bin/env python

"""
Echo Server
"""

import socket


if __name__ == '__main__':
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)

    buffsize = 32
    try:
        while True:
            response = ''
            done = False
            conn, addr = server_socket.accept()
            print conn
            while not done:
                msg_part = conn.recv(buffsize)
                if len(msg_part) < buffsize:
                    done = True
                response += msg_part
            conn.sendall(response)
            conn.close()
    except KeyboardInterrupt:
        pass
    server_socket.close()
