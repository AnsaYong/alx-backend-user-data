#!/usr/bin/env python3
"""
Session Authentication module
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates and stores a new session ID for a user_id

        Args:
            user_id (str): user_id to create session for

        Returns:
            str: the session ID created
        """
        if user_id is None or type(user_id) is not str:
            return None

        session_id = uuid.uuid4()
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = user_id

        return session_id
