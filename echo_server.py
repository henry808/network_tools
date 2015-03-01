#!/usr/bin/env python

"""
Echo Server
"""

import socket
import email.utils


BUFFERSIZE = 32


def echo_server():
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


# Update the server loop you built for the echo server so that it:
# gathers an incoming request
# tries to parse the request and catches any errors raised
# builds a "200 OK"  response if parsing worked
# builds an appropriate HTTP error if an error was raised
# returns the constructed response to the client.

def response_ok():
    """return a well formed HTTP "200 OK" response as a byte string
    """
    lines = [
        "HTTP/1.1 200 OK",
        "Date : {}".format(email.utils.formatdate(usegmt=True)),
        "Content-Type: text/xml; charset=utf-8",
        "<html><body><h1>Successful response.</h1></body></html>"
    ]

    return "".join(["\r\n".join(lines), "\r\n\r\n"])


def response_error(code=400, message="Bad Request"):
    """return a well formed HTTP error response"""
    error = " ".join([str(code), message])
    lines = [
        "HTTP/1.1 {}".format(error),
        "Date : {}".format(email.utils.formatdate(usegmt=True)),
        "Content-Type: text/xml; charset=utf-8",
        "<html><body><h1> {} </h1></body></html>".format(error)
    ]

    return "".join(["\r\n".join(lines), "\r\n\r\n"])


def parse_request(request):
    """parse an HTTP request and return the URI requested.

    If not a GET request raise an HTTPError.
    If not a HTTP/1.1 request, raise an HTTPError."""
    request_list = request.split()
    try:
        if request_list[0] != 'GET':
            raise HTTPError('Not a get request.')
        if request_list[2] != 'HTTP/1.1':
            raise HTTPError('Not HTTP/1.1 protocal.')
    except IndexError:
        raise HTTPError('HTTP Request not complete.')
    return request_list[1]


class HTTPError(StandardError):
    pass

if __name__ == '__main__':
    echo_server()
