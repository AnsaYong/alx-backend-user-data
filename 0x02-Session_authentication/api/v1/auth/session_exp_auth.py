#!/usr/bin/env python
"""
This module is responsible for the session expiration authentication
"""
from flask import request, jsonify
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime
import os
from datetime import timedelta


class SessionExpAuth(SessionAuth):
    """
    This class is responsible for the session expiration authentication,
    based on an expiration time
    """

    def __init__(self):
        """
        Initialize the session duration from the environment variable
        """
        session_duration = os.getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except (TypeError, ValueError):
            self.session_duration = 0


    def create_session(self, user_id: str = None) -> str:
        """
        Create a session with a timestamp

        Args:
            user_id (str): the user id

        Returns:
            str: the session id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get the user id for a session id, if session is valid

        Args:
            session_id (str): the session id

        Returns:
            str: the user id
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return session_dict.get('user_id')
