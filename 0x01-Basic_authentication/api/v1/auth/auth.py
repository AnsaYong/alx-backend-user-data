#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manages the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Handles the authentication requirements

        Returns:
            - True if the path is not excluded and the path
            is not in the excluded paths
            - False otherwise
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Handles the Authorization header

        Returns:
            - The value of the Authorization header
            - None if the Authorization header is not present
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Handles the current user

        Returns:
            - The current user
            - None if the request is not authorized
        """
        return None
