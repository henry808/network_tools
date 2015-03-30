#!/usr/bin/env python

"""
Echo Server
"""

import socket
import email.utils
import io
import os
import mimetypes

BUFFERSIZE = 32
# This is not a secure solution because a client could look at any directory 
# using commands like ../ to get above the root
ROOT_DIR = "webroot/"

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
                response = response_ok(parsed_request)
            except HTTPError400:
                response = response_error(400, 'Bad Request')
            except HTTPError404:
                response = response_error(405, 'Not Found')
            except HTTPError405:
                response = response_error(405, 'Method not allowed')
            except HTTPError415:
                response = response_error(415, 'Unsupported media type')
            except HTTPError505:
                response = response_error(505, 'HTTP version not supported')
            conn.sendall(response)
            conn.close()
    except KeyboardInterrupt:
        pass
    server_socket.close()


def resolve_uri(uri):
    """Given a URI, return a body and content type.

    If the URI is a directory, return that directory as a list as the body.
    If the URI a file, return the contents of the file as the body
    Content type is the file type.
    Raises type error if uri is not a string.
    Raises an IO error if the uri is not a file or directory.
    Raises an IO error if cannot find a mimetype.
    """
    if not isinstance(uri, str):
        raise HTTPError404('Not found')
    uri = os.path.join(ROOT_DIR, uri)
    extension = os.path.splitext(uri)
    try:
        content_type = mimetypes.types_map[extension[1]]
    except KeyError:
        content_type = ''
    if os.path.isfile(uri):  # if uri is a file
        if content_type == 'text/plain' or content_type == 'text/html':
                with io.open(uri, 'r') as file1:
                    body = file1.read()
        elif content_type == 'image/jpeg' or content_type == 'image/png':
                with io.open(uri, 'rb') as file1:
                    body = file1.read()
        else:
            raise HTTPError415('Unsupported media type')
    elif os.path.isdir(uri):  # if uri is a directory
        content_type = 'directory'
        dir_list = os.listdir(uri)
        for index, item in enumerate(dir_list):
            dir_list[index] = "<li>{}</li>".format(item)
        body = "<ul>{}</ul>".format("".join(dir_list))
    else:  # if uri is not a dir or a file
        raise HTTPError404('Not found')
    return body, content_type


def response_ok(uri):
    """return a well formed HTTP "200 OK" response as a byte string
    """
    body, content_type = resolve_uri(uri)
    if content_type == 'text/plain' or content_type == 'text/html':
        content_type = "".join([content_type, '; charset=utf-8'])
        body = body.encode('utf-8')

    lines = [
        "HTTP/1.1 200 OK",
        "Date : {}".format(email.utils.formatdate(usegmt=True)),
        "Content-Type: {}; charset=utf-8".format(content_type),
        "Content-Length: {}".format(len(body)),
        "",
        body,
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


class HTTPError404(HTTPError):
    pass


class HTTPError405(HTTPError):
    pass


class HTTPError415(HTTPError):
    pass


class HTTPError505(HTTPError):
    pass


if __name__ == '__main__':
    echo_server()
