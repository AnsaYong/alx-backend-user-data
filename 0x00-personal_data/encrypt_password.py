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
