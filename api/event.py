"""
Written by: Group 404

This file handles the API requests for getting, editing and deleting event information

"""
# import third party libraries
from flask_restful import Resource, reqparse

# import custom classes used to interact with the DB
from db.db_events import EventsDB


class Event(Resource):
    def get(self):

        # parse request
        event_id = self.parse_get_delete()

        # create db engine
        events_db = EventsDB()

        if event_id:
            # if event_id provided
            result = events_db.select_event_id(event_id)
        else:
            # if neither event_id or event_name provided return error
            return {
                "resultStatus": "Error",
                "message": "Both event ID and event name were not supplied, please supply one",
            }

        if not result:
            return {"resultStatus": "ERROR", "message": "event not found"}

        # finally return result
        return {"resultStatus": "SUCCESS", "event_details": result}

    def put(self):

        # parse request
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str)
        parser.add_argument("detail", type=dict)
        parser.add_argument("event_id", type=str)
        args = parser.parse_args()

        token = args["token"]
        event_details = args["detail"]
        event_id = args["event_id"]

        # create db engine
        events_db = EventsDB()

        result = events_db.update_event(event_id, event_details, token)
        if result == True:
            return {
                "resultStatus": "SUCCESS",
            }
        else:
            return {
                "resultStatus": "ERROR",
            } 

    def delete(self):

        # parse request
        event_id = self.parse_get_delete()

        # create db engine
        events_db = EventsDB()

        if event_id:
            # if event_id provided
            result = events_db.delete_event_id(event_id)
            event_details = event_id
        else:
            # if neither event_id or event_name provided return error
            return {
                "resultStatus": "Error",
                "message": "Both event ID and event name were not supplied, please supply one",
            }

        if result == True:
            # If result is True, return SUCCESS and event details
            return {
                "resultStatus": "SUCCESS",
                "event": event_details,
                "message": "event deleted",
            }

        if "Error" in result:
            # if result != True, return ERROR and error message
            return {"resultStatus": "ERROR", "message": result,}

    def parse_get_delete(self):
        # parse the event_id and/or event_name arguments
        parser = reqparse.RequestParser()
        parser.add_argument("event_id", type=int, location="args")
        args = parser.parse_args()

        # assign variables
        event_id = args["event_id"]

        return event_id
