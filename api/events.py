'''
Written by: Group 404

This file handles the API requests for returning all events 

'''

from flask_restful import Resource
from db.init_db import InitDB


class Events(Resource):
    def get(self):
        temp_db = InitDB()
        result = temp_db.select_all_events()

        return {
            'resultStatus': 'SUCCESS',
            'message': result
        }