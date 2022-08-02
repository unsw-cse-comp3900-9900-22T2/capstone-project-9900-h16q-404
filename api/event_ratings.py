# import third party libraries
from flask_restful import Resource, reqparse
from flask import request
import datetime

from db.db_token_handler import TokenHandlerDB
from db.db_reviews import ReviewsDB
from db.db_event_ratings import EventRatingsDB

class EventRatings(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('eventId', type=int, location='args')
        args = parser.parse_args()
        # assign variables
        eventId = args['eventId']

        # create db engine
        reviews_db = ReviewsDB()
        event_ratings_db = EventRatingsDB()
        
        # check event exists
        event_exists = reviews_db.check_eventid_exists(eventId)
        if event_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'Event Id does not exist'
            }
        
        # get event host and type by id
        eventDetails = reviews_db.select_event_byId(eventId)
        
        if (len(eventDetails) < 0):
            return {
                'resultStatus': 'ERROR',
                'message': 'Unable to Retreive Event Details'
            }
        
        host = eventDetails[0]['host']
        eventType = eventDetails[0]['type']
        hostName = eventDetails[0]['host_username']
        
        result_dict = {}
        result_dict['Host Name'] = hostName
        result_dict['Event Type'] = eventType
        
        # get ratings based on host and event type
        eventRatings = event_ratings_db.select_ratings_from_reviews(host, eventType)
        numRatings = len(eventRatings)
        
        # Compute Average Rating
        average_rating = 0
        
        if (len(eventRatings) > 0):
            sum_ratings = 0
            for rating in eventRatings:
                sum_ratings += rating['rating']
            average_rating = sum_ratings / numRatings
        
        result_dict['Average Rating'] = round(average_rating, 2)
        
        return {
            'resultStatus': 'SUCCESS',
            'message': result_dict
        }