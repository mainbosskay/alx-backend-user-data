#!/usr/bin/env python3
"""Module for API authentication operations management"""
from flask import request
import re
from typing import List, TypeVar


class Auth:
    """Class for managing authentication operations"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is requred for a given path"""
        if path is not None and excluded_paths is not None:
            for excldPath in map(lambda k: k.strip(), excluded_paths):
                matchPattrn = ""
                if excldPath[-1] == "*":
                    matchPattrn = f"{excldPath[0:-1]}.*"
                elif excldPath[-1] == "/":
                    matchPattrn = f"{excldPath[0:-1]}/*"
                else:
                    matchPattrn = f"{excldPath}/*"
                if re.match(matchPattrn, path):
                    return False
        return True


    def authorization_header(self, request=None) -> str:
        """Getting and return auth header from incoming request"""
        if request is not None:
            return request.headers.get("Authorization", None)
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """Identifying present user based on the request"""
        return None
