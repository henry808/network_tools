import pytest
from echo_client import echo_client
from echo_server import response_ok, response_error, parse_request
from echo_server import HTTPError505, HTTPError400, HTTPError405
from echo_server import resolve_uri, HTTPError404, HTTPError415
import io


# response_ok tests
def test_response_ok_directory(directory_list):
    "directory returns list"
    uri = 'webroot'
    response = response_ok(uri)
    dir_list = directory_list
    assert 'HTTP/1.1 200 OK' in response
    assert 'Content-Type: directory; charset=utf-8' in response
    assert '' in response
    assert dir_list in response


def test_response_ok_text():
    "text file"
    uri = 'webroot/sample.txt'
    response = response_ok(uri)
    with io.open(uri, 'r') as file1:
        expected_body = file1.read()
        size = len(expected_body)
    assert 'HTTP/1.1 200 OK' in response
    assert 'Content-Type: text/plain; charset=utf-8' in response
    assert 'Content-Length: {}'.format(size) in response
    assert '' in response
    assert expected_body in response


def test_response_ok_html():
    "text file"
    uri = 'webroot/a_web_page.html'
    response = response_ok(uri)
    with io.open(uri, 'r') as file1:
        expected_body = file1.read()
        size = len(expected_body)
    assert 'HTTP/1.1 200 OK' in response
    assert 'Content-Type: text/html; charset=utf-8' in response
    assert 'Content-Length: {}'.format(size) in response
    assert '' in response
    assert expected_body in response


def test_response_ok_jpg_image():
    "jpg file"
    uri = 'webroot/images/JPEG_example.jpg'
    response = response_ok(uri)
    with io.open(uri, 'rb') as file1:
        expected_body = file1.read()
        size = len(expected_body)
    assert 'HTTP/1.1 200 OK' in response
    assert 'Content-Type: image/jpeg; charset=utf-8' in response
    assert 'Content-Length: {}'.format(size) in response
    assert '' in response
    assert expected_body in response


def test_response_ok_png_image():
    "png file"
    uri = 'webroot/images/sample_1.png'
    response = response_ok(uri)
    with io.open(uri, 'rb') as file1:
        expected_body = file1.read()
        size = len(expected_body)
    assert 'HTTP/1.1 200 OK' in response
    assert 'Content-Type: image/png; charset=utf-8' in response
    assert 'Content-Length: {}'.format(size) in response
    assert '' in response
    assert expected_body in response


# resolve_uri tests
def test_resolve_uri_directory(directory_list):
    """directory"""
    uri = 'webroot'
    body, content_type = resolve_uri(uri)
    expected_body = directory_list
    assert body == expected_body
    assert content_type == 'directory'


def test_resolve_uri_html():
    """html content type"""
    uri = 'webroot/a_web_page.html'
    body, content_type = resolve_uri(uri)
    with io.open(uri, 'r') as file1:
        expected_body = file1.read()
    assert body == expected_body
    assert content_type == 'text/html'


def test_resolve_uri_txt():
    """text content type"""
    uri = 'webroot/sample.txt'
    body, content_type = resolve_uri(uri)
    with io.open(uri, 'r') as file1:
        expected_body = file1.read()
    assert body == expected_body
    assert content_type == 'text/plain'


def test_resolve_uri_jpg_small():
    """small jpeg content type"""
    uri = 'webroot/images/JPEG_example.jpg'
    body, content_type = resolve_uri(uri)
    with io.open(uri, 'rb') as file1:
        expected_body = file1.read()
    assert body == expected_body
    assert content_type == 'image/jpeg'


def test_resolve_uri_jpg_big():
    """big content type"""
    uri = 'webroot/images/Sample_Scene_Balls.jpg'
    body, content_type = resolve_uri(uri)
    with io.open(uri, 'rb') as file1:
        expected_body = file1.read()
    assert body == expected_body
    assert content_type == 'image/jpeg'


def test_resolve_uri_png():
    """png content type"""
    uri = 'webroot/images/sample_1.png'
    body, content_type = resolve_uri(uri)
    with io.open(uri, 'rb') as file1:
        expected_body = file1.read()
    assert body == expected_body
    assert content_type == 'image/png'


def test_resolve_uri_empty_string():
    """empty string io error"""
    uri = ''
    with pytest.raises(HTTPError404):
        body, content_type = resolve_uri(uri)


def test_resolve_uri_unsupported_mimetype():
    """non string error"""
    uri = 'webroot/images/test.gif'
    with pytest.raises(HTTPError415):
        body, content_type = resolve_uri(uri)


def test_resolve_uri_non_string():
    """non string error"""
    uri = 333
    with pytest.raises(HTTPError404):
        body, content_type = resolve_uri(uri)
    uri = {'notstring': 'not a string'}
    with pytest.raises(HTTPError404):
        body, content_type = resolve_uri(uri)


def test_resolve_uri_non_existing_file():
    """file or directory does not exist error"""
    uri = 'this_file_does_not_exist.txt'
    with pytest.raises(HTTPError404):
        body, content_type = resolve_uri(uri)


# server reponse tests
def test_server_dir(GET_request_webroot, directory_list):
    """Test a server resonse for a directory """
    text = GET_request_webroot
    assert 'HTTP/1.1 200 OK' in echo_client(text)
    assert 'Content-Type: directory; charset=utf-8' in echo_client(text)
    assert '' in echo_client(text)
    assert directory_list in echo_client(text)


def test_server_text(GET_request_text):
    """Test a server resonse for a text file """
    text = GET_request_text
    uri = 'webroot/sample.txt'
    with io.open(uri, 'r') as file1:
        expected_body = file1.read()
    size = len(expected_body)
    assert 'HTTP/1.1 200 OK' in echo_client(text)
    assert 'Content-Type: text/plain; charset=utf-8' in echo_client(text)
    assert 'Content-Length: {}'.format(size) in echo_client(text)
    assert '' in echo_client(text)
    assert expected_body in echo_client(text)


def test_server_text(GET_request_html):
    """Test a server resonse for an html """
    text = GET_request_html
    uri = 'webroot/a_web_page.html'
    with io.open(uri, 'r') as file1:
        expected_body = file1.read()
    size = len(expected_body)
    assert 'HTTP/1.1 200 OK' in echo_client(text)
    assert 'Content-Type: text/html; charset=utf-8' in echo_client(text)
    assert 'Content-Length: {}'.format(size) in echo_client(text)
    assert '' in echo_client(text)
    assert expected_body in echo_client(text)


def test_server_png(GET_request_png):
    """Test a server resonse for a png"""
    text = GET_request_png
    uri = 'webroot/images/sample_1.png'
    with io.open(uri, 'rb') as file1:
        expected_body = file1.read()
    size = len(expected_body)
    assert 'HTTP/1.1 200 OK' in echo_client(text)
    assert 'Content-Type: image/png; charset=utf-8' in echo_client(text)
    assert 'Content-Length: {}'.format(size) in echo_client(text)
    assert '' in echo_client(text)
    assert expected_body in echo_client(text)


def test_server_jpg(GET_request_jpg):
    """Test a server resonse for a png"""
    text = GET_request_jpg
    uri = 'webroot/images/JPEG_example.jpg'
    with io.open(uri, 'rb') as file1:
        expected_body = file1.read()
    size = len(expected_body)
    assert 'HTTP/1.1 200 OK' in echo_client(text)
    assert 'Content-Type: image/jpeg; charset=utf-8' in echo_client(text)
    assert 'Content-Length: {}'.format(size) in echo_client(text)
    assert '' in echo_client(text)
    assert expected_body in echo_client(text)


def test_server_200(GET_request_right_protocal):
    """Test that a good request returns 200"""
    text = GET_request_right_protocal
    assert '200' in echo_client(text)
    assert 'OK' in echo_client(text)


def test_server_400():
    """Test that a bad request returns a 400"""
    text = ""
    assert '400' in echo_client(text)
    assert 'Bad Request' in echo_client(text)


def test_server_missing_blank_line(GET_request_missing_blank_line_before_body):
    """Test that a request missing a blank line returns a 400"""
    text = GET_request_missing_blank_line_before_body
    assert '400' in echo_client(text)
    assert 'Bad Request' in echo_client(text)


def test_server_missing_body(GET_request_is_missing_a_body):
    """Test that a request missing a body returns a 400"""
    text = GET_request_is_missing_a_body
    assert '400' in echo_client(text)
    assert 'Bad Request' in echo_client(text)


def test_server_405(POST_request_right_protocal):
    """Test that a non-GET request returns a 405"""
    text = POST_request_right_protocal
    assert '405' in echo_client(text)
    assert 'Method not allowed' in echo_client(text)


def test_server_505(GET_request_wrong_protocal):
    """Test that a GET request with wrong protocal returns a 505"""
    text = GET_request_wrong_protocal
    assert '505' in echo_client(text)
    assert 'HTTP version not supported' in echo_client(text)


def test_response_error():
    """Test returns error response"""
    assert "HTTP/1.1 400 Bad Request" in response_error()
    assert "Content-Type: text/xml; charset=utf-8" in response_error()
    assert "<html><body><h1> 400 Bad Request </h1></body></html>" in response_error()

    assert "<html><body><h1> 404 Not Found </h1></body></html>" in response_error(404, "Not Found")


def test_parse(empty_request):
    """empty request raises an error: 400"""
    with pytest.raises(HTTPError400):
        request = parse_request(empty_request)


def test_parse_no_empty_line(GET_request_missing_blank_line_before_body):
    """no empty line before body request raises an error: 400"""
    with pytest.raises(HTTPError400):
        request = parse_request(GET_request_missing_blank_line_before_body)


def test_parse_no_body(GET_request_is_missing_a_body):
    """no body request raises an error: 400"""
    with pytest.raises(HTTPError400):
        request = parse_request(GET_request_is_missing_a_body)


def test_parse_wrong_protocao(GET_request_wrong_protocal):
    """GET request wrong protocal: 505"""
    with pytest.raises(HTTPError505):
        request = parse_request(GET_request_wrong_protocal)


def test_parse_post_request_right_protocal(POST_request_right_protocal):
    """POST request right protocal: 405"""
    with pytest.raises(HTTPError405):
        request = parse_request(POST_request_right_protocal)


def test_parse_wrong_protocal(POST_request_wrong_protocal):
    """POST request wrong protocal: 405"""
    with pytest.raises(HTTPError405):
        request = parse_request(POST_request_wrong_protocal)


def test_parse_good(GET_request_right_protocal):
    """GET request right protocal: return the URI"""
    request = parse_request(GET_request_right_protocal)
    assert request == "webroot/sample.txt"


# requests used for testing
@pytest.fixture(scope='function')
def GET_request_webroot():
    uri = 'webroot'
    lines = [
        "GET {} HTTP/1.1".format(uri),
        "Host: www.test.com",
        "",
        "<body>Get this resource.</body>",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def GET_request_txt():
    uri = 'webroot/sample.txt'
    lines = [
        "GET {} HTTP/1.1".format(uri),
        "Host: www.test.com",
        "",
        "<body>Get this resource.</body>",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def GET_request_html():
    uri = 'webroot/a_web_page.html'
    lines = [
        "GET {} HTTP/1.1".format(uri),
        "Host: www.test.com",
        "",
        "<body>Get this resource.</body>",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def GET_request_png():
    uri = 'webroot/images/sample_1.png'
    lines = [
        "GET {} HTTP/1.1".format(uri),
        "Host: www.test.com",
        "",
        "<body>Get this resource.</body>",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def GET_request_jpg():
    uri = 'webroot/images/JPEG_example.jpg'
    lines = [
        "GET {} HTTP/1.1".format(uri),
        "Host: www.test.com",
        "",
        "<body>Get this resource.</body>",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def empty_request():
    lines = [
        ""
    ]
    return "".join(["\r\n".join(lines), "\r\n\r\n"])


@pytest.fixture(scope='function')
def GET_request_right_protocal():
    lines = [
        "GET webroot/sample.txt HTTP/1.1",
        "Host: www.test.com",
        "",
        "<body>This is a legal request</body>",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def GET_request_wrong_protocal():
    lines = [
        "GET webroot/sample.txt IMAPS",
        "Host: www.test.com",
        "",
        "This test had a bad protocal",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def POST_request_right_protocal():
    lines = [
        "POST webroot/sample.txt HTTP/1.1",
        "Host: www.test.com",
        "",
        "This test is a well formed POST request.",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def POST_request_wrong_protocal():
    lines = [
        "POST webroot/sample.txt IMAPS",
        "Host: www.test.com",
        "",
        "This request is a POST Request with a bad protocal.",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def GET_request_missing_blank_line_before_body():
    lines = [
        "GET webroot/sample.txt HTTP/1.1",
        "Host: www.test.com",
        "<body>This is a malformed request missing a blank line.</body>",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def GET_request_is_missing_a_body():
    lines = [
        "GET webroot/sample.txt HTTP/1.1",
        "Host: www.test.com",
        "",
        "\r\n"
    ]
    return "\r\n".join(lines)


@pytest.fixture(scope='function')
def directory_list():
    listing = ['.DS_Store', 'a_web_page.html', 'images', 'make_time.py', 'sample.txt']
    for index, item in enumerate(listing):
        listing[index] = "<li>{}</li>".format(item)
    body = "<ul>{}</ul>".format("".join(listing))
    return body
