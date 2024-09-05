#!/usr/bin/env python3
"""Module for managing user login and session mgt in session auth views"""
from api.v1.views import app_views
from typing import Tuple
from flask import request, jsonify, abort
import os
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login() -> Tuple[str, int]:
    """Managing user login via POST request to /api/v1/auth_session/login"""
    NFresUser = {"error": "no user found for this email"}
    email = request.form.get("email")
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        UsersList = User.search({"email": email})
    except Exception:
        return jsonify(NFresUser), 404
    if len(UsersList) <= 0:
        return jsonify(NFresUser), 404
    if UsersList[0].is_valid_password(password):
        from api.v1.app import auth
        sessionToken = auth.create_session(getattr(UsersList[0], "id"))
        resLogin = jsonify(UsersList[0].to_json())
        resLogin.set_cookie(os.getenv("SESSION_NAME"), sessionToken)
        return resLogin
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
        "/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """Manages user logout via DELETE request to /api/v1/auth_session/logout"""
    from api.v1.app import auth
    terminatedSessn = auth.destroy_session(request)
    if not terminatedSessn:
        abort(404)
    return jsonify({})
