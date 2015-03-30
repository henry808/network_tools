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
            request = ''
            done = False
            conn, addr = server_socket.accept()
            while not done:
                msg_part = conn.recv(BUFFERSIZE)
                if len(msg_part) < BUFFERSIZE:
                    done = True
                request += msg_part
            try:
                parsed_request = parse_request(request)
                response = response_ok()
            except HTTPError400:
                response = response_error(400, 'Bad Request')
            except HTTPError405:
                response = response_error(405, 'Method not allowed')
            except HTTPError505:
                response = response_error(505, 'HTTP version not supported')
            conn.sendall(response)
            conn.close()
    except KeyboardInterrupt:
        pass
    server_socket.close()


def response_ok(body=''):
    """return a well formed HTTP "200 OK" response as a byte string
    """
    lines = [
        "HTTP/1.1 200 OK",
        "Date : {}".format(email.utils.formatdate(usegmt=True)),
        "Content-Type: text/xml; charset=utf-8",
        "",
        "<html><body><h1>Successful response.</h1></body></html>",
        "\r\n"
    ]

    return "\r\n".join(lines)


def response_error(code=400, message="Bad Request"):
    """return a well formed HTTP error response"""
    error = " ".join([str(code), message])
    lines = [
        "HTTP/1.1 {}".format(error),
        "Date : {}".format(email.utils.formatdate(usegmt=True)),
        "Content-Type: text/xml; charset=utf-8",
        "",
        "<html><body><h1> {} </h1></body></html>".format(error),
        "\r\n"
    ]

    return "\r\n".join(lines)



def parse_request(request):
    """parse an HTTP request and return the URI requested.

    If not a GET request raise an HTTPError405.
    If not a HTTP/1.1 request, raise an HTTPError505.
    If request is not properly formed raise an HTTPError400
    If not GET and not HTTP/1.1 request then raise an HTTPError404

    """
    request_list = request.split("\r\n")
    try:
        # if GET is not the first word on first line, 405
        if request_list[0].split()[0] != 'GET':
            raise HTTPError405('Method not allowed')
        # if HTTP/1.1 is not the third word on first line, 505
        if request_list[0].split()[2] != 'HTTP/1.1':
            raise HTTPError505('HTTP version not supported')
        # if the fourth line is not an empty string, 400
        if request_list[3] == '':
            raise HTTPError400('Bad Request')
        # See if a fifth line exists, if not, we are out of index
        # This is where the body shoud be.
        body = request_list[5]
    except IndexError:
        # if there is missing info, then it's a bad request for sure
        raise HTTPError400('Bad Request')
    return request_list[0].split()[1]


class HTTPError(StandardError):
    pass


class HTTPError400(HTTPError):
    pass


class HTTPError405(HTTPError):
    pass


class HTTPError505(HTTPError):
    pass


if __name__ == '__main__':
    echo_server()
