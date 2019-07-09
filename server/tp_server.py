#!/usr/bin/env python
"""
To Run:
    
    export FLASK_RUN_PORT=####
    export FLAS_APP=tp_server.py
    flask run

"""

from flask import Flask
from flask_restful import Resource, Api
app = Flask(__name__)



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

@app.route("/")
def intro():
    return "<h1>Welcome to our boat site</h1>"








api.add_resource(main, '/')



