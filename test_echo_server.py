import pytest
from echo_client import echo_client


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
