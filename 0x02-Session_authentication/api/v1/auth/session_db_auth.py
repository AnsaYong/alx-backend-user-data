#!/usr/bin/env python3
"""
This module is responsible for the session database authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    This class is responsible for the session database authentication
    """
    def create_session(self, user_id: str = None) -> str:
        """
        Create a session with a user id

        Args:
            user_id (str): the user id

        Returns:
            str: the session id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create and save a new UserSession instance
        new_user_session = UserSession(user_id=user_id, session_id=session_id)
        new_user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get the user id for a session id from the database, if session is valid
        """
        if session_id is None:
            return None

        # Find the UserSession instance with the session_id
        user_session = UserSession.search({'session_id': session_id})
        if user_session is None:
            return None

        user_session = user_session[0]
        # Check if the session is still valid
        if self.session_duration <= 0:
            return user_session.user_id

        if user_session.created_at + timedelta(
                    seconds=self.session_duration) < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroy a session
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_session = UserSession.search({'session_id': session_id})
        if user_session is None:
            return False

        user_session = user_session[0]
        user_session.remove()

        return True
