'''
Written by: Group 404

This file handles the API requests for getting, editing and deleting event information

'''

from flask_restful import Resource, reqparse
from db.init_db import InitDB
from db.db_events import EventsDB


class Event(Resource):
    def get(self):
        # parse the event_id and/or event_name arguments
        parser = reqparse.RequestParser()
        parser.add_argument('event_name', type=str, location="args")
        parser.add_argument('event_id', type=int, location="args")
        args = parser.parse_args()

        # assign variables
        event_name = args['event_name']
        event_id = args['event_id']

        # create db engine
        temp_db = InitDB()

        if event_id and event_name:
            # if both parameters are provided, return error
            return {
            'resultStatus': 'Error',
            'message': 'Both event ID and event name supplied, please supply only one'
            }
        elif event_name:
            # if event_name provided
            result = temp_db.select_event_name(event_name)
        elif event_id:
            # if event_id provided
            result = temp_db.select_event_id(event_id)
        else:
            # if neither event_id or event_name provided return error
            return {
            'resultStatus': 'Error',
            'message': 'Both event ID and event name were not supplied, please supply one'
            }

        if not result:
            return {
            'resultStatus': 'ERROR',
            'message': 'event not found'
        }

        # finally return result
        return {
            'resultStatus': 'SUCCESS',
            'event_details': result
        }

    def put(self):
        # parse the event_id and/or event_name arguments
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        parser.add_argument('detail', type=dict)
        parser.add_argument('event_id', type=str)
        args = parser.parse_args()

        # assign variables
        token = args['token']
        event_details = args['detail']
        event_id = args['event_id']

        # create db engine
        events_db = EventsDB()

        result = events_db.update_event(event_id, event_details, token)
        if result == True:
            return {
            'resultStatus': 'SUCCESS',
            }
        else:
            return {
            'resultStatus': 'ERROR',
            } 

    def delete(self):
        # parse the event_id and/or event_name arguments
        parser = reqparse.RequestParser()
        parser.add_argument('event_name', type=str, location="args")
        parser.add_argument('event_id', type=int, location="args")
        args = parser.parse_args()

        # assign variables
        event_name = args['event_name']
        event_id = args['event_id']

        # create db engine
        events_db = EventsDB()

        if event_id and event_name:
            # if both parameters are provided, return error
            return {
            'resultStatus': 'Error',
            'message': 'Both event ID and event name supplied, please supply only one'
            }
        elif event_name:
            # if event_name provided
            result = events_db.delete_event_name(event_name)
            event_details = event_name
        elif event_id:
            # if event_id provided
            result = events_db.delete_event_id(event_id)
            event_details = event_id
        else:
            # if neither event_id or event_name provided return error
            return {
            'resultStatus': 'Error',
            'message': 'Both event ID and event name were not supplied, please supply one'
            }

        if result == True:
        # If result is True, return SUCCESS and event details
            return {
                'resultStatus': 'SUCCESS',
                'event': event_details,
                'message': 'event deleted'
            }

        if "Error" in result:
        # if result != True, return ERROR and error message
            return {
                'resultStatus': 'ERROR',
                'message': result
            }