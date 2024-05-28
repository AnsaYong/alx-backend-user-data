#!/usr/bin/env python3
"""
A simple Flask application to demonstrate the use of SQLAlchemy.
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    Return a greeting message.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
