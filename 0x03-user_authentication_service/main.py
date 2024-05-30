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


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Log in with wrong password

    Args:
        email (str): Email of the user
        password (str): Password of the user
    """
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert response.status_code == 401, f"Expected 401, got (response.status_code)"


def log_in(email: str, password: str) -> Optional[str]:
    """
    Log in with correct password

    Args:
        email (str): Email of the user
        password (str): Password of the user

    Returns:
        str: Session ID
    """
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "session_id" in response.cookies, "No session_id cookie found"
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """
    Profile of an unlogged user
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"


def profile_logged(session_id: str) -> None:
    """
    Profile of a logged user

    Args:
        session_id (str): Session ID
    """
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json() == {
        "email": EMAIL,
    }, f"Unexpected response: {response.json()}"


def log_out(session_id: str) -> None:
    """
    Log out

    Args:
        session_id (str): Session ID
    """
    response = requests.delete(
        f"{BASE_URL}/sessions", cookies={"session_id": session_id}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json() == {
        "message": "Bienvenue",
    }, f"Unexpected response: {response.json()}"


def reset_password_token(email: str) -> str:
    """
    Request a password reset token

    Args:
        email (str): Email of the user

    Returns:
        str: Reset token
    """
    response = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the password of a user

    Args:
        email (str): Email of the user
        reset_token (str): Reset token
        new_password (str): New password
    """
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email, "reset_token": reset_token, "new_password": new_password},
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json() == {
        "email": email,
        "message": "Password updated",
    }, f"Unexpected response: {response.json()}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
