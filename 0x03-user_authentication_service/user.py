#!/usr/bin/env python3
"""
This module provides a SQLAlchemy model for a user.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# Define the declarative base class
Base = declarative_base()


# Define the User model
class User(Base):
    """
    A model to represent a user.

    Attributes:
        id (int): The user's ID.
        email (str): The user's email address.
        hashed_password (str): The user's hashed password.
        session_id (str): The user's session ID.
        reset_token (str): The user's reset token.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
