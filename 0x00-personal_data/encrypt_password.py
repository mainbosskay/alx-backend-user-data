#!/usr/bin/env python3
"""Module for encrypting password securely with bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Getting and return salted, hashed password with bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
