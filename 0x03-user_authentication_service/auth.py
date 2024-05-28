#!/usr/bin/env python3
"""
This module provides the Auth methods.
"""
import bcrypt


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
