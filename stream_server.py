#!/usr/bin/env python

from echo_server import parse_request
from gevent.monkey import patch_all
from gevent.server import StreamServer
from echo_server import response_ok, response_error, parse_request
from echo_server import HTTPError505, HTTPError400, HTTPError405
from echo_server import HTTPError404, HTTPError415

BUFFER_SIZE = 32


def handler(socket, address):
    request = ""
    
    while True:
        data = socket.recv(BUFFER_SIZE)
        if data:
            request += data
        else:
            break
    try:
        parsed_request = parse_request(request)
        response = response_ok(parsed_request)
    except HTTPError400:
        response = response_error(400, 'Bad Request')
    except HTTPError404:
        response = response_error(404, 'Not Found')
    except HTTPError405:
        response = response_error(405, 'Method not allowed')
    except HTTPError415:
        response = response_error(415, 'Unsupported media type')
    except HTTPError505:
        response = response_error(505, 'HTTP version not supported')
    socket.sendall(response)
    socket.close()
    


if __name__ == '__main__':
    try:
        patch_all()
        server = StreamServer(('127.0.0.1', 50000), handler)
        server.serve_forever()
    except KeyboardInterrupt:
        pass
