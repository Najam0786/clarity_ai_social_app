# test_main.py

"""
Author: Nazmul Mustufa Farooquee
Date: 2025-03-28
"""

import sys
import os
from io import StringIO
import pytest

# Ensure path for importing main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import SocialApp


# ---------------- Fixtures ---------------- #


@pytest.fixture
def app_fixture():
    """Initialize a clean SocialApp instance."""
    instance = SocialApp()
    instance.user_messages.clear()
    instance.user_follows.clear()
    return instance


# ---------------- Test Cases ---------------- #


def test_posting_message(app_fixture):
    app_fixture.handle_posting("Alice", "Hello World")
    assert "Alice" in app_fixture.user_messages
    assert len(app_fixture.user_messages["Alice"]) == 1
    assert app_fixture.user_messages["Alice"][0][1] == "Hello World"


def test_reading_timeline_valid_user(app_fixture):
    app_fixture.handle_posting("Bob", "Test message")
    captured_output = StringIO()
    sys.stdout = captured_output
    app_fixture.handle_reading("Bob")
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    assert "Bob" in output
    assert "Test message" in output


def test_reading_timeline_no_posts(app_fixture):
    captured_output = StringIO()
    sys.stdout = captured_output
    app_fixture.handle_reading("Unknown")
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    assert "No posts found" in output


def test_following_user(app_fixture):
    app_fixture.handle_following("Alice", "Bob")
    assert "Bob" in app_fixture.user_follows.get("Alice", [])


def test_follow_self(app_fixture):
    app_fixture.handle_following("Alice", "Alice")
    assert "Alice" not in app_fixture.user_follows.get("Alice", [])


def test_combined_wall(app_fixture):
    app_fixture.handle_posting("Alice", "Hi")
    app_fixture.handle_posting("Bob", "Hey")
    app_fixture.handle_following("Alice", "Bob")
    captured_output = StringIO()
    sys.stdout = captured_output
    app_fixture.show_wall("Alice")
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    assert "Hi" in output
    assert "Hey" in output
