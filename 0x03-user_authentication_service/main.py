#!/usr/bin/env python3
"""
Main file
"""
import requests
from typing import Optional


BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """
    Register a new user

    Args:
        email (str): Email of the user
        password (str): Password of the user
    """
    response = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password}
    )
    assert response.status_code == 200, f"Expected 200, got (response.status_code)"
    assert response.json() == {
        "email": email,
        "message": "user created",
    }, f"Unexpected response: {response.json()}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
