"""
Written by: Group 404

This file handles the API requests for getting reserved ticket information for a user

"""
# import third party libraries
from flask_restful import Resource
from flask import request

# import custom classes used to interact with the DB
from db.db_events import EventsDB


class SearchEvent(Resource):
    def post(self):

        # parse request
        getRequest = request.json
        if "keyWordList" in getRequest:
            searchTerms = getRequest["keyWordList"]
        else:
            return {"status": "Error", "message": "Search Key Word List was not Sent"}

        # create db engines
        events_db = EventsDB()

        allEvents = events_db.select_all_events()
        result = []

        if len(searchTerms) > 0:
            for event in allEvents:
                eventsStrToSearch = " ".join(
                    (event["event_name"], event["description"], event["type"])
                )
                eventsStrToSearch = eventsStrToSearch.lower()
                queryinEvent = False
                for item in searchTerms:
                    if item in eventsStrToSearch:
                        queryinEvent = True
                        break
                if queryinEvent:
                    result.append(event)

        return {"resultStatus": "SUCCESS", "message": result}
