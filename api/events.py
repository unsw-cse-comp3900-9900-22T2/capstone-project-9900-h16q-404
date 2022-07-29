'''
Written by: Group 404

This file handles the API requests for returning all events 

'''

from flask_restful import Resource
from db.init_db import InitDB
from db.db_events import EventsDB

class Events(Resource):
    def get(self):
        events_db = EventsDB()
        result = events_db.select_all_events()

        return {
            'resultStatus': 'SUCCESS',
            'message': result
        }