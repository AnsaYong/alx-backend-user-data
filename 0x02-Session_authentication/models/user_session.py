#!/usr/bin/env python3
"""
This module is responsible for the user session
"""
from models.base import Base
import uuid


class UserSession(Base):
    """
    This class is responsible for the user session
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a new UserSession instance
        Args:
            args (list): the list of arguments
            kwargs (dict): the dictionary of keyword arguments
        
        Attributes:
            user_id (str): the user id
            session_id (str): the session id
        """
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        super().__init__(*args, **kwargs)
