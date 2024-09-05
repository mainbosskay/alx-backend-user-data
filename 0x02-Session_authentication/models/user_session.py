#!/usr/bin/env python3
"""Module for user sessions management"""
from models.base import Base


class UserSession(Base):
    """Class for user sessions representation"""

    def __init__(self, *args: list, **kwargs: dict) -> None:
        """Initialising user session class"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
