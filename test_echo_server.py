import pytest
from echo_client import echo_client
from echo_server import response_ok, response_error, parse_request
from echo_server import BUFFERSIZE, HTTPError
import echo_server


def test_server_text():
    """Test that a byte string works"""
    text = "this is a test"
    assert echo_client(text) == text


def test_server_empty():
    """Test that an empty string works"""
    text = ""
    assert echo_client(text) == text


def test_server_unicode():
    """Test that a unicode string works"""
    text = u"this is a test for a unicode string: \u00bd\u0553\u04e7"
    text = text.encode('utf-8')
    assert echo_client(text) == text


def test_server_long_string():
    """Test that a string longer than 32 works"""
    text = u"this is a test of whether a string longer than 32 workds"
    assert echo_client(text) == text


def test_server_buffer_size_string():
    """Test that a string longer than 32 works"""
    list1 = []
    for i in range(0, BUFFERSIZE):
        list1.append('a')
    text = ''.join(list1)
    assert len(text) == BUFFERSIZE
    assert echo_client(text) == text


def test_response_ok():
    """Test returns ok response"""
    assert '200 OK' in response_ok()


def test_response_error():
    """Test returns error response"""
    assert '400' in response_error()
    assert 'Bad Request' in response_error()
    assert '404' in response_error(404, "Not Found")
    assert 'Not Found' in response_error(404, "Not Found")


def test_parse(empty_request,
               GET_request_right_protocal,
               GET_request_wrong_protocal,
               POST_request_right_protocal,
               POST_request_wrong_protocal):
    """tests parse"""
    # empty request raises an error
    with pytest.raises(HTTPError):
        request = parse_request(empty_request)
    # GET request wrong protocal
    with pytest.raises(HTTPError):
        request = parse_request(GET_request_wrong_protocal)
    # POST request right protocal
    with pytest.raises(HTTPError):
        request = parse_request(POST_request_right_protocal)
    # POST request wrong protocal
    with pytest.raises(HTTPError):
        request = parse_request(POST_request_wrong_protocal)
    # GET request right protocal
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
    ]
    return "".join(["\r\n".join(lines), "\r\n\r\n"])


@pytest.fixture(scope='function')
def GET_request_wrong_protocal():
    lines = [
        "GET /index.html IMAPS",
        "Host: www.test.com",
    ]
    return "".join(["\r\n".join(lines), "\r\n\r\n"])


@pytest.fixture(scope='function')
def POST_request_right_protocal():
    lines = [
        "POST /index.html HTTP/1.1",
        "Host: www.test.com",
    ]
    return "".join(["\r\n".join(lines), "\r\n\r\n"])


@pytest.fixture(scope='function')
def POST_request_wrong_protocal():
    lines = [
        "POST /index.html IMAPS",
        "Host: www.test.com",
    ]
    return "".join(["\r\n".join(lines), "\r\n\r\n"])
