#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    Manages the API Basic authentication
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the base64 part from the Authorization header

        Args:
            - authorization_header: The Authorization header

        Returns:
            - The base64 part of the Authorization header
            - None if the header is not present
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a base64 string

        Args:
            - base64_authorization_header: The base64 string to decode

        Returns:
            - The decoded string
            - None if the string is not correctly base64 encoded
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user credentials from a decoded base64 string

        Args:
            - decoded_base64_authorization_header: The decoded base64 string

        Returns:
            - A tuple containing the user email and password from the decoded
              base64 string
            - None if the decoded string is not valid
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves the user object from the credentials

        Args:
            - user_email: The user email
            - user_pwd: The user password

        Returns:
            - The user object if the credentials are valid
            - None if the credentials are not valid
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        from models.user import User
        users = User.search({'email': user_email})
        if not users:
            return None

        # Assume that there should only be one user with the given email
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user
