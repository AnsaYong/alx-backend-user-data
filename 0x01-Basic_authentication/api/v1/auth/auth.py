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
            - True if the path is None
            - True if the path is not in the list of excluded paths
            - True if excluded paths is None or empty
            - False otherwise
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure path has a trailing slash for comparison
        if not path.endswith('/'):
            path += '/'

        # Iterate over excluded paths to check for matches
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Handles the Authorization header.
        Validates all requests to secure the API

        Returns:
            - The value of the Authorization header
            - None if the Authorization header is not present
        """
        if request is None or request.headers.get('Authorization') is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Handles the current user

        Returns:
            - The current user
            - None if the request is not authorized
        """
        return None
