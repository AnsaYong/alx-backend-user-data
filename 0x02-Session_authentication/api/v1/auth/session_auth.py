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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID

        Args:
            session_id (str): the session ID to look up

        Returns:
            str: the User ID
        """
        if session_id is None or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)
