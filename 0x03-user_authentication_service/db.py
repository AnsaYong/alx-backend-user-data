#!/usr/bin/env python3
"""
This module provides the DB class.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """
    A class to represent a database.

    Attributes:
        _engine (Engine): The database engine.
        _session (Session): The database session.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created user object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        session.refresh(new_user)  # Refresh the user object to get the ID
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by the given keyword arguments.

        Args:
            **kwargs: The keyword arguments to search for.

        Returns:
            User: The first user object.

        Raises:
            NoResultFound: If no user is found with the given criteria.
            InvalidRequestError: If the request is invalid.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the given criteria.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid request.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user by the given user ID.

        Args:
            user_id (int): The user's ID.
            **kwargs: The keyword arguments to update.

        Returns:
            None

        Raises:
            ValueError: If the attribute is invalid.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")

        self._session.commit()
