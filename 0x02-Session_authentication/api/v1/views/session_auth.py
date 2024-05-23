#!/usr/bin/env python3
"""
Session Authentication module
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login/',
                 methods=['POST'], strict_slashes=False)
def login():
    """
    POST /api/v1/auth_session/login/
    Handles user login by creating a session ID
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if user is None or not user:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]  # Assuming the search returns a list of users

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    if not session_id:
        abort(500)

    response = jsonify(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response
