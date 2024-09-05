#!/usr/bin/env python3
"""Module for API session authentication expiration ops management"""
from .session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """Class for managing session authentication expiration operations"""

    def __init__(self) -> None:
        """Initializing session authentication expiration class"""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """Generating & store seesion id & creation time for given user"""
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Getting user id linked with a given session id & creation time"""
        if session_id in self.user_id_by_session_id:
            dictSession = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return dictSession["user_id"]
            if "created_at" not in dictSession:
                return None
            timeNow = datetime.now()
            spanSessn = timedelta(seconds=self.session_duration)
            expryTime = dictSession["created_at"] + spanSessn
            if expryTime < timeNow:
                return None
            return dictSession["user_id"]
