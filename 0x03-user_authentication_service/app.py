#!/usr/bin/env python3
"""
A simple Flask application to demonstrate the use of SQLAlchemy.
"""
from flask import Flask, jsonify, request, abort, make_response
from flask import redirect, url_for
import uuid
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """
    Return a greeting message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    POST /users route for registering a new user.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    POST /sessions route for logging in a user.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    response = make_response(jsonify({"email": email, "message": "logged in"}),
                             200)
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    DELETE /sessions route for logging out a user.
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    # Invalidate the session
    AUTH._db.update_user(user.id, session_id=None)

    return redirect(url_for("home"))


@app.route("/profile", methods=["GET"])
def profile():
    """
    GET /profile route to return the user's profile.
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """
    POST /reset_password route to generate a reset password token.
    """
    email = request.form.get("email")

    if not email:
        abort(400, "Email is required")

    try:
        user = AUTH._db.find_user_by(email=email)
    except NoResultFound:
        abort(403)

    reset_token = str(uuid.uuid4())
    AUTH._db.update_user(user.id, reset_token=reset_token)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """
    PUT /reset_password route to update the user's password.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        abort(400, "Email, reset_token, and new_password are required")

    try:
        AUTH.update_password(password=new_password, reset_token=reset_token)
    except ValueError:
        abort(403, description="Invalid reset_token")

    return jsonify({"email": email, "message": "password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
