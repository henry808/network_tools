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
    # if not 'HTTP/1.1' in request:
    #     raise HTTPError("Malformed HTTP request")
    # if not 'GET' in request:
    #     raise HTTPError("Not a get request")
    return request_list


class HTTPError(StandardError):
    pass

if __name__ == '__main__':
    print response_error()
    echo_server()
