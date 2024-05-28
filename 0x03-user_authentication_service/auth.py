#!/usr/bin/env python3
"""
This module handles user authorisation.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> str:
    """
    Hash the given password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    Generate a random UUID.

    Returns:
        str: The generated UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database
    """

    def __init__(self):
        """
        Initialize a new Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the given email and password.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            User: The newly created user object.

        Raises:
            ValueError: If the email is already registered.
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check if the given email and password are valid.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if the email and password are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False
