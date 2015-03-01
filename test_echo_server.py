import pytest
from echo_client import echo_client
from echo_server import BUFFERSIZE


def test_server_text():
    """Test that a byte string works"""
    text = "this is a test"
    assert echo_client(text) == text


def test_server_empty():
    """Test that an empty string works"""
    text = ""
    assert echo_client(text) == text


def test_server_unicode():
    """Test that a unicode string works:"""
    text = u"this is a test for a unicode string: \u00bd\u0553\u04e7"
    text = text.encode('utf-8')
    assert echo_client(text) == text


def test_server_long_string():
    """Test that a string longer than 32 works"""
    text = u"this is a test of whether a string longer than 32 works"
    assert echo_client(text) == text


def test_server_buffer_size_string():
    """Test that a string longer than 32 works"""
    list1 = []
    for i in range(0, BUFFERSIZE):
        list1.append('a')
    text = ''.join(list1)
    assert len(text) == BUFFERSIZE
    assert echo_client(text) == text
