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
            while not done:
                conn, addr = server_socket.accept()
                msg_part = conn.recv(buffsize)
                if len(msg_part) < buffsize:
                    done = True
                    conn.sendall(response)
                    conn.close()
                response += msg_part
            conn.close()
    except KeyboardInterrupt:
        pass
    server_socket.close()
