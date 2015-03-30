import pytest
from echo_client import echo_client
from echo_server import response_ok, response_error, parse_request
from echo_server import HTTPError505, HTTPError400, HTTPError405


def test_server_200(GET_request_right_protocal):
    """Test that a good request returns 200"""
    text = GET_request_right_protocal
    assert '200' in echo_client(text)
    assert 'OK' in echo_client(text)


def test_server_400():
    """Test that a bad request returns a 400"""
    text = ""
    assert '400' in echo_client(text)
    assert 'HTTP Request malformed.' in echo_client(text)


def test_server_missing_blank_line(GET_request_missing_blank_line_before_body):
    """Test that a request missing a blank line returns a 400"""
    text = GET_request_missing_blank_line_before_body
    assert '400' in echo_client(text)
    assert 'HTTP Request malformed.' in echo_client(text)


def test_server_missing_body(GET_request_is_missing_a_body):
    """Test that a request missing a body returns a 400"""
    text = GET_request_is_missing_a_body
    assert '400' in echo_client(text)
    assert 'HTTP Request malformed.' in echo_client(text)


def test_server_405(POST_request_right_protocal):
    """Test that a non-GET request returns a 405"""
    text = POST_request_right_protocal
    assert '405' in echo_client(text)
    assert 'Not a GET request.' in echo_client(text)


def test_server_505(GET_request_wrong_protocal):
    """Test that a GET request with wrong protocal returns a 505"""
    text = GET_request_wrong_protocal
    assert '505' in echo_client(text)
    assert 'Not HTTP/1.1 protocal.' in echo_client(text)


def test_response_ok():
    """Test returns ok response"""
    assert 'HTTP/1.1 200 OK' in response_ok()
    assert 'Content-Type: text/xml; charset=utf-8' in response_ok()
    assert '<html><body><h1>Successful response.</h1></body></html>' in response_ok()


def test_response_error():
    """Test returns error response"""
    assert "HTTP/1.1 400 Bad Request" in response_error()
    assert "Content-Type: text/xml; charset=utf-8" in response_error()
    assert "<html><body><h1> 400 Bad Request </h1></body></html>" in response_error()

    assert "<html><body><h1> 404 Not Found </h1></body></html>" in response_error(404, "Not Found")


def test_parse(empty_request,
               GET_request_right_protocal,
               GET_request_wrong_protocal,
               POST_request_right_protocal,
               POST_request_wrong_protocal):
    """tests parse"""
    # empty request raises an error: 400
    with pytest.raises(HTTPError400):
        request = parse_request(empty_request)
    # GET request wrong protocal: 505
    with pytest.raises(HTTPError505):
        request = parse_request(GET_request_wrong_protocal)
    # POST request right protocal: 405
    with pytest.raises(HTTPError405):
        request = parse_request(POST_request_right_protocal)
    # POST request wrong protocal: 405
    with pytest.raises(HTTPError405):
        request = parse_request(POST_request_wrong_protocal)
    # GET request right protocal: return the URI
    request = parse_request(GET_request_right_protocal)
    assert request == "/index.html"


# test requests
@pytest.fixture(scope='function')
def empty_request():
    lines = [
        ""
    ]
    return "".join(["\r\n".join(lines), "\r\n\r\n"])


@pytest.fixture(scope='function')
def GET_request_right_protocal():
    lines = [
        "GET /index.html HTTP/1.1",
        "Host: www.test.com",
        "",
        "<body>This is a legal request</body>",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def GET_request_wrong_protocal():
    lines = [
        "GET /index.html IMAPS",
        "Host: www.test.com",
        "",
        "This test had a bad protocal",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def POST_request_right_protocal():
    lines = [
        "POST /index.html HTTP/1.1",
        "Host: www.test.com",
        "",
        "This test is a well formed POST request.",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def POST_request_wrong_protocal():
    lines = [
        "POST /index.html IMAPS",
        "Host: www.test.com",
        "",
        "This request is a POST Request with a bad protocal.",
        "\r\n"
    ]
    return "\r\n".join(lines)

@pytest.fixture(scope='function')
def GET_request_missing_blank_line_before_body():
    lines = [
        "GET /index.html HTTP/1.1",
        "Host: www.test.com",
        "<body>This is a malformed request missing a blank line.</body>",
        "\r\n"
    ]
    return "\r\n".join(lines)

@pytest.fixture(scope='function')
def GET_request_is_missing_a_body():
    lines = [
        "GET /index.html HTTP/1.1",
        "Host: www.test.com",
        "<body>This is a malformed request missing a blank line.</body>",
        "",
        "\r\n"
    ]
    return "\r\n".join(lines)