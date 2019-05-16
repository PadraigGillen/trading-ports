#!/usr/bin/env python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def intro():
    return "<h1>Welcome to our boat site</h1>"
