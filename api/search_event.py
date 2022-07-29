'''
Written by: Group 404

This file handles the API requests for getting reserved ticket information for a user

'''

from flask_restful import Resource
from db.init_db import InitDB
from flask import request
from db.db_events import EventsDB


class SearchEvent(Resource):
    def post(self):
        getRequest = request.json
        if ('keyWordList' in getRequest):
            searchTerms = getRequest['keyWordList']
        else:
            return {"status": "Error", "message": "Search Key Word List was not Sent"}
        
        # create db engine
        events_db = EventsDB()
        
        allEvents = events_db.select_all_events()
        result = []
        
        if (len(searchTerms) > 0):
            for event in allEvents:
                eventsStrToSearch = " ". join((event['event_name'], event['description'], event['type']))
                eventsStrToSearch = eventsStrToSearch.lower()
                queryinEvent = False
                for item in searchTerms:
                    if item in eventsStrToSearch:
                        queryinEvent = True
                        break;
                if queryinEvent:
                    result.append(event)
        
        return {
            'resultStatus': 'SUCCESS',
            'message': result
        }