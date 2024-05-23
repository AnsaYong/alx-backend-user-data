#!/usr/bin/env python3
"""
Session Authentication module
"""
from api.v1.auth.auth import Auth
from models.user import User
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

        session_id = str(uuid.uuid4())
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

    def current_user(self, request=None):
        """
        Retrieve the curren user from the request

        Args:
            request (obj): the request object

        Returns:
            User instance or None
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the user session / logout

        Args:
            request (obj): the request object

        Returns:
            None
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]

        return True
