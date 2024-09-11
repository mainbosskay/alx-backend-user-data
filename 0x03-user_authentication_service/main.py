#!/usr/bin/env python3
"""Module for `app.py` test end-to-end integration"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL_BASE = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Testing registration of user functionality"""
    endpoint = f"{URL_BASE}/users"
    payload = {"email": email, "password": password}
    res = requests.post(endpoint, data=payload)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    res = requests.post(endpoint, data=payload)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Testing login using incorrect password"""
    endpoint = f"{URL_BASE}/sessions"
    payload = {"email": email, "password": password}
    res = requests.post(endpoint, data=payload)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Testing login functionality"""
    endpoint = f"{URL_BASE}/sessions"
    payload = {"email": email, "password": password}
    res = requests.post(endpoint, data=payload)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """Testing profile info retrieval when not logged in"""
    endpoint = f"{URL_BASE}/profile"
    res = requests.get(endpoint)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Testing profile info retrieval when logged in"""
    endpoint = f"{URL_BASE}/profile"
    payload = {"session_id": session_id}
    res = requests.get(endpoint, cookies=payload)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """Testing logout functionality"""
    endpoint = f"{URL_BASE}/sessions"
    payload = {"session_id": session_id}
    res = requests.delete(endpoint, cookies=payload)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Testing reset on password token generation"""
    endpoint = f"{URL_BASE}/reset_password"
    payload = {"email": email}
    res = requests.post(endpoint, data=payload)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Testing update on user password functionality"""
    endpoint = f"{URL_BASE}/reset_password"
    payload = {"email": email, "reset_token": reset_token,
               "new_password": new_password}
    res = requests.put(endpoint, data=payload)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
