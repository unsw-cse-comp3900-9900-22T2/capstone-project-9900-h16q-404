"""
Written by: Group 404

This file handles the API requests for creating a new event

"""
# import third party libraries
from flask_restful import Resource, reqparse

# import custom classes used to interact with the DB
from db.db_events import EventsDB


class Create(Resource):
    def post(self):

        # parse the event_id and/or event_name arguments
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, location='headers')
        parser.add_argument("detail", type=dict)
        args = parser.parse_args()

        # assign variables
        token = args["token"]
        event_details = args["detail"]

        # create db engine
        events_db = EventsDB()

        try:
            new_id, insert_data = events_db.create_event(token, event_details)
            insert_data["start_date"] = str(insert_data["start_date"])
            insert_data["start_time"] = str(insert_data["start_time"])[:-3]
            insert_data["end_date"] = str(insert_data["end_date"])
            insert_data["end_time"] = str(insert_data["end_time"])[:-3]

            return {
                "resultStatus": "SUCCESS",
                "new_event_id": new_id,
                "event_details": insert_data,
            }
        except:
            return {
                "resultStatus": "ERROR",
                "message": "failed to insert new event into events table",
            }
