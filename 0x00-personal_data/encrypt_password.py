#!/usr/bin/env python3
"""Module for encrypting password securely with bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Getting and return salted, hashed password with bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validating plain password using hashed password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
