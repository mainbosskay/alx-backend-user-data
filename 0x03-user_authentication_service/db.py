#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Inserting into database a new user record"""
        try:
            userRecord = User(email=email, hashed_password=hashed_password)
            self._session.add(userRecord)
            self._session.commit()
        except Exception:
            self._session.rollback()
            userRecord = None
        return userRecord

    def find_user_by(self, **kwargs) -> User:
        """Retriving user matching the specified criteria"""
        columns, valsFilter = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                columns.append(getattr(User, key))
                valsFilter.append(value)
            else:
                raise InvalidRequestError()
        userRecord = self._session.query(User).filter(
                tuple_(*columns).in_([tuple(valsFilter)])).first()
        if userRecord is None:
            raise NoResultFound()
        return userRecord

    def update_user(self, user_id: int, **kwargs) -> None:
        """Modifying user record which is identified by user_id"""
        userRecord = self.find_user_by(id=user_id)
        if userRecord is None:
            return
        updtSource = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                updtSource[getattr(User, key)] = value
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
                updtSource, synchronize_session=False)
        self._session.commit()
