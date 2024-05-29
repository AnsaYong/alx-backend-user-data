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

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user with the given email.

        Args:
            email (str): The user's email address.

        Returns:
            str: The session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get the user associated with the given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            User: The user associated with the session ID.
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
            return None
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session for the user with the given ID.

        Args:
            user_id (int): The ID of the user.
        """
        self._db.update_user(user_id, session_id=None)
