'''
Written by: Group 404

This file handles the API requests for the filer feature on the landing page

'''

from flask_restful import Resource, reqparse
from db.init_db import InitDB


class Filter(Resource):
    def get(self):
        # parse the event filter type arguments
        parser = reqparse.RequestParser()
        parser.add_argument('filterType', type=str, location="args")
        args = parser.parse_args()

        # assign variables
        filter_type = args['filterType']
        
        # create db engine
        temp_db = InitDB()
        
        # Get events hosted by this user
        result = temp_db.select_events_bytype(filter_type)
        
        if not result:
            return {
            'resultStatus': 'ERROR',
            'message': 'No Events Match Filter Type'
        }

        # finally return result
        return {
            'resultStatus': 'SUCCESS',
            'event_details': result
        }