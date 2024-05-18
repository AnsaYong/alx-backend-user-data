#!/usr/bin/env python3
"""
This module provides functions that handle password encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password with a randomly genereated salt

    Args:
        password (str): the plaintext password to hash

    Returns:
        bytes: the salted, hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a password matches a hashed password

    Args:
        hashed_password (bytes): the hashed password
        password (str): the plaintext password to check

    Returns:
        bool: True if the password matches the hashed password, False otherwise
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
