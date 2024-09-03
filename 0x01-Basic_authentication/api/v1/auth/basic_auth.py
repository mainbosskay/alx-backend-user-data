#!/usr/bin/env python3
"""Module for API basic authentication operations management"""
from .auth import Auth
import re
from typing import Tuple, TypeVar
from models.user import User
import binascii
import base64


class BasicAuth(Auth):
    """Class for managing basic authentication operations"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Getting & return base64 token from auth header for basic auth"""
        if type(authorization_header) == str:
            regexPttrn = r"Basic (?P<token>.+)"
            fldMch = re.fullmatch(regexPttrn, authorization_header.strip())
            if fldMch is not None:
                return fldMch.group("token")
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Converting base64-encoded auth header into decode string"""
        if type(base64_authorization_header) == str:
            try:
                decodedBytes = base64.b64decode(base64_authorization_header,
                                                validate=True)
                return decodedBytes.decode("utf-8")
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """Extract username & password from decoded base64 auth header"""
        if type(decoded_base64_authorization_header) == str:
            regexPttrn = r"(?P<user>[^:]+):(?P<password>.+)"
            fldMch = re.fullmatch(regexPttrn,
                                  decoded_base64_authorization_header.strip())
            if fldMch is not None:
                usr = fldMch.group("user")
                pwd = fldMch.group("password")
                return usr, pwd
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Getting & return user based on user's auth information"""
        if type(user_email) == str and type(user_pwd) == str:
            try:
                mchUsers = User.search({"email": user_email})
            except Exception:
                return None
            if len(mchUsers) <= 0:
                return None
            if mchUsers[0].is_valid_password(user_pwd):
                return mchUsers[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Getting & returns present user based on request"""
        authHeader = self.authorization_header(request)
        b64Token = self.extract_base64_authorization_header(authHeader)
        decodedToken = self.decode_base64_authorization_header(b64Token)
        email, pwd = self.extract_user_credentials(decodedToken)
        return self.user_object_from_credentials(email, pwd)
