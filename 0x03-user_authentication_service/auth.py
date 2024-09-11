#!/usr/bin/env python3
"""Module for authentication-related routines management"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Encrypting and return password salted hash"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
