
from flask_restful import Resource, reqparse
from flask import request
from collections import defaultdict

from db.db_user_ratings import UserRatingsDB


class UserRatings(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=int, location='args')
        args = parser.parse_args()
    
        # assign variables
        userId = args['userId']
        
        # create db engine
        user_ratings_db = UserRatingsDB()

        
        user_ratings = user_ratings_db.select_ratings_by_host(userId)
        numEvents = len(user_ratings)
        overall_rating = 0
        
        result_dict = {}
        event_type_rating_dict = defaultdict(float)
        event_type_count_dict = defaultdict(int)
        
        if (numEvents > 0):
            sum_ratings = 0
            for rating in user_ratings:
                sum_ratings += rating['rating']
                event_type_rating_dict[rating['eventType']] += rating['rating']
                event_type_count_dict[rating['eventType']] += 1
            overall_rating = sum_ratings / numEvents
        
        
        for key, val in event_type_rating_dict.items():
            temp = event_type_rating_dict[key]
            newVal = temp / event_type_count_dict[key]
            event_type_rating_dict[key] = round(newVal, 2)

        result_dict['Overall Rating'] = round(overall_rating, 2)
        result_dict['Event Type Rating'] = event_type_rating_dict
        
        return {
            'resultStatus': 'SUCCESS',
            'message': result_dict
        }