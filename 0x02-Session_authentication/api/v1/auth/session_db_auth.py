#!/usr/bin/env python3
"""Module for handling API session authentication expiration & storage ops"""
from .session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Class for managing session authentication expiration & storage ops"""

    def create_session(self, user_id=None) -> str:
        """Generating & storing a session ID for user, saving it in db"""
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            sessionInfo = {
                    "user_id": user_id,
                    "session_id": session_id
            }
            userSessn = UserSession(**sessionInfo)
            userSessn.save()
            return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Getting user id linked with given session id & creation time"""
        try:
            dictSession = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if len(dictSession) <= 0:
            return None
        timeNow = datetime.now()
        spanSessn = timedelta(seconds=self.session_duration)
        expryTime = dictSession[0].created_at + spanSessn
        if expryTime < timeNow:
            return None
        return dictSession[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Deleting authenticated session"""
        session_id = self.session_cookie(request)
        try:
            dictSession = UserSession.search({"session_id": session_id})
        except Exception:
            return False
        if len(dictSession) <= 0:
            return False
        dictSession[0].remove()
        return True
