#!/usr/bin/env python

"""
Echo Server
"""

import socket
import email.utils


def echo_server():
    """echo server echos a short string back through a socket"""
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


def response_ok():
    """return a well formed HTTP "200 OK" response as a byte string
    """
    lines = [
        "HTTP/1.1 200 OK",
        "Date : {}".format(email.utils.formatdate(usegmt=True)),
        "Content-Type: text/xml; charset=utf-8",
        "<html><body><h1>Successful response.</h1></body></html>"
    ]

    return "".join(["\r\n".join(lines), "\r\n"])


def response_error(code=400, message="Bad request"):
    """return a well formed HTTP error response"""
    error = " ".join([str(code), message])
    lines = [
        "HTTP/1.1 {}".format(error),
        "Date : {}".format(email.utils.formatdate(usegmt=True)),
        "Content-Type: text/xml; charset=utf-8",
        "<html><body><h1> {} </h1></body></html>".format(error)
    ]

    return "".join(["\r\n".join(lines), "\r\n"])


def parse_request(request):
    """parse an HTTP request and return the URI requested.

    Must be a GET requests, if not raise an appropriate Python error.
    Must be HTTP/1.1 requests, a request of any other protocol should
    raise an appropriate error"""
    request_list = request.split("\r\n")
    if not 'HTTP/1.1' in request:
        raise HTTPError
    if not 'GET' in request:
        raise HTTPError
    return ""


class HTTPError(StandardError):
    pass


raise HTTPError("Malformed HTTP request")

if __name__ == '__main__':
    print response_error()
    echo_server()