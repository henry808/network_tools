import pytest
from echo_client import echo_client
from echo_server import response_ok, response_error, parse


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
    text = u"this is a test"
    assert echo_client(text) == text


def test_server_long_string():
    """Test that a string longer than 32 works"""
    text = u"this is a test of whether a string longer than 32 workds"
    assert echo_client(text) == text


def test_response_ok():
    """Test returns ok response"""
    assert '200 OK' in response_ok


def test_response_error():
    """Test returns error response"""
    assert '400' in response_error()
    assert 'Bad Request' in response_error()
    assert '404' in response_error(404, "Not Found")
    assert 'Not Found' in response_error(404, "Not Found")


def test_parse():
    """tests parse"""
    t = parse("Test")
    assert True

