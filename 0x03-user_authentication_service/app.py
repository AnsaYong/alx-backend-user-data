#!/usr/bin/env python3
"""
A simple Flask application to demonstrate the use of SQLAlchemy.
"""
from flask import Flask, jsonify, request, abort, make_response
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

    if not AUTH.get_user_by_email(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    response = make_response(jsonify({"email": email, "message": "logged in"}), 200)
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
