"""
Written by: Group 404

This file handles the API requests for returning all events 

"""
# import third party libraries
from flask_restful import Resource

# import custom classes used to interact with the DB
from db.db_events import EventsDB

class Events(Resource):
    def get(self):

        # create db engines
        events_db = EventsDB()
        
        result = events_db.select_all_events()

        return {
            "resultStatus": "SUCCESS",
            "message": result
        }