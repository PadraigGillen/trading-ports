#!/usr/bin/env python
"""
To Run:
    
    export FLASK_RUN_PORT=####
    export FLAS_APP=tp_server.py
    flask run

"""

from flask import Flask, render_template, g
from flask_restful import Resource, Api, reqparse, abort
import sqlite3

app = Flask(__name__)
api = Api(app)

# =====> using the 'g' object to auto-open/close SQL connection

# https://flask-doc.readthedocs.io/en/latest/patterns/sqlite3.html
# using this site as a reference so to avoid the routes being cluttered with db work
@app.before_request
def before_request():
    g.db = sqlite3.connect("database.db")

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
def get():
    return "<h1>Hello! <a href='/boats'>Have a peek at our boats?</a></h1>"

BOATS = {
    'boat1': {'boat': 'skipper'},
    'boat2': {'boat': 'destroyer'},
    'boat3': {'boat': 'profiteer'},
}


def abort_if_boat_doesnt_exist(boat_id):
    if boat_id not in BOATS:
        abort(404, message="boat {} doesn't exist".format(boat_id))

parser = reqparse.RequestParser()
parser.add_argument('boat')


# boat
# shows a single boat item and lets you delete a boat item
class boat(Resource):
    def get(self, boat_id):
        abort_if_boat_doesnt_exist(boat_id)
        return BOATS[boat_id]

    def delete(self, boat_id):
        abort_if_boat_doesnt_exist(boat_id)
        del BOATS[boat_id]
        return '', 204

    def put(self, boat_id):
        args = parser.parse_args()
        boat = {'boat': args['boat']}
        BOATS[boat_id] = boat
        return boat, 201

# boatList
# shows a list of all boats, and lets you POST to add new boats
class boatList(Resource):
    def get(self):
        return BOATS

    def post(self):
        args = parser.parse_args()
        boat_id = int(max(BOATS.keys()).lstrip('boat')) + 1
        boat_id = 'boat%i' % boat_id
        BOATS[boat_id] = {'boat': args['boat']}
        return BOATS[boat_id], 201

api.add_resource(boatList, '/boats/')
api.add_resource(boat, '/boats/<boat_id>')


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


if __name__ == "__main__":
    app.run(debug=True)
