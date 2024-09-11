#!/usr/bin/env python3
"""Module for authentication-related routines management"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Encrypting and return password salted hash"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


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
