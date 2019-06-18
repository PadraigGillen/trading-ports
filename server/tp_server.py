#!/usr/bin/env python
"""
To Run:
    
    export FLASK_RUN_PORT=####
    export FLAS_APP=tp_server.py
    flask run

"""

from flask import Flask, render_template, g
from flask_restful import Resource, Api
import sqlite3

app = Flask(__name__)


# =====> using the 'g' object to auto-open/close SQL connection

# https://flask-doc.readthedocs.io/en/latest/patterns/sqlite3.html
# using this site as a reference so to avoid the routes being cluttered with db work
@app.before_request
def before_request():
    g.db = sqlite3.connect(database.db)

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


# =====> helper functions
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


# =====> Routes

@app.route("/")
def intro():
    return "<h1>Welcome to our boat site</h1>"

"""
[GET REQUESTS]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@get info about boat
.../boat/{ID}

@get info about all boats
...

@get info about user

@get info about all users

@get info about ocean
- DEPRICATED

@get info about everything

@get info about boat

@get info about all boats

[BOAT MANIPULATION]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@create boat
.../boat (post)
 - Boat attributes are determined via the server
    - likely random

@move a boat
.../boat/{ID}/{location}/{ID} (put)
- Location can be:
    sea (ID: 0)
    harbor (ID)
    slip (ID)
- Location must be considered connected to current location:
    slip <-> harbor <-> sea
- timed event based on daemon

@delete a boat
.../boat/{ID} (delete)
- determined by daemon
    - calculated based on total number of boats

@update a boat
.../boat/{ID} (Patch)

@delete all boats
.../boat (delete)
- will require auth

[Port manipulation]
~~~~~~~~~~~~~~~~~~~~~~~~~~
@delete a slip
.../slip/{ID} (delete)
- requires auth
- cannot be used if there is a boat in the slip

@create a slip
.../slip (post)
- requires auth


"""

