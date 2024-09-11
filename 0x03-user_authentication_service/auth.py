#!/usr/bin/env python3
"""Module for authentication-related routines management"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """Encrypting and return password salted hash"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Getting and return unique uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializing an Auth instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Creating and storing databases new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Verification of a user's login details validity"""
        userRecord = None
        try:
            userRecord = self._db.find_user_by(email=email)
            if userRecord is not None:
                return bcrypt.checkpw(password.encode("utf-8"),
                                      userRecord.hashed_password)
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Creating a given users new session"""
        userRecord = None
        try:
            userRecord = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if userRecord is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(userRecord.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Getting and return user using session ID"""
        userRecord = None
        if session_id is None:
            return None
        try:
            userRecord = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return userRecord

    def destroy_session(self, user_id: int) -> None:
        """Terminating specific user linked session"""
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Creating reset token password for specified email"""
        userRecord = None
        try:
            userRecord = self._db.find_user_by(email=email)
        except NoResultFound:
            userRecord = None
        if userRecord is None:
            raise ValueError()
        resetTokPwd = _generate_uuid()
        self._db.update_user(userRecord.id, reset_token=resetTokPwd)
        return resetTokPwd

    def update_password(self, reset_token: str, password: str) -> None:
        """Updating user's password with provided reset token"""
        instUser = None
        try:
            instUser = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            instUser = None
        if instUser is None:
            raise ValueError()
        newPWDhash = _hash_password(password)
        self._db.update_user(instUser.id, hashed_password=newPWDhash,
                             reset_token=None)
