#!/usr/bin/env python3
"""Flask app with user authentication capabilities"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """Home page content"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def create_user() -> str:
    """Payload that indicates account creation status"""
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """Payload that indicates login status"""
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    newSessionID = AUTH.create_session(email)
    respLogin = jsonify({"email": email, "message": "logged in"})
    respLogin.set_cookie("session_id", newSessionID)
    return respLogin


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """Logouts session and redirecting to home route"""
    sessionCookie = request.cookies.get("session_id")
    userSession = AUTH.get_user_from_session_id(sessionCookie)
    if userSession is None:
        abort(403)
    AUTH.destroy_session(userSession.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """Getting and return information on user's profile"""
    sessionIDNow = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(sessionIDNow)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """Payload for request of password reset"""
    userEmail = request.form.get("email")
    resetTokPwd = None
    try:
        resetTokPwd = AUTH.get_reset_password_token(userEmail)
    except ValueError:
        resetTokPwd = None
    if resetTokPwd is None:
        abort(403)
    return jsonify({"email": userEmail, "reset_token": resetTokPwd})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """Payload that indicates success or failure of password update"""
    userEmail = request.form.get("email")
    resetTokPwd = request.form.get("reset_token")
    pwdNew = request.form.get("new_password")
    updatedPwd = False
    try:
        AUTH.update_password(resetTokPwd, pwdNew)
        updatedPwd = True
    except ValueError:
        updatedPwd = False
    if not updatedPwd:
        abort(403)
    return jsonify({"email": userEmail, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
