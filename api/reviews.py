

# import third party libraries
from flask_restful import Resource, reqparse
from flask import request
import datetime

from db.db_token_handler import TokenHandlerDB
from db.db_reviews import ReviewsDB

class Reviews(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='args')
        parser.add_argument('eventId', type=int, location='args')
        args = parser.parse_args()
        # assign variables
        token = args['token']
        eventId = args['eventId']

        # create db engine
        token_db = TokenHandlerDB()
        reviews_db = ReviewsDB()

        
        # check user exists
        user_exists = token_db.check_usertoken_exists(token)
        
        result_dict = {}
        result_dict['hostedBy'] = reviews_db.get_event_hostname(eventId)
        
        if user_exists:
            user_id = token_db.get_host_id_from_token(token)
            result_dict['is_host'] = reviews_db.check_user_isHost(user_id, eventId)
            result_dict['has_ticket'] = reviews_db.check_user_hasTicket(user_id, eventId)
            result_dict['has_comment'] = reviews_db.check_user_hasComment(user_id, eventId)
        else:
            result_dict['is_host'] = False
            result_dict['has_ticket'] = False
            result_dict['has_comment'] = False
        
        result_dict['reviews'] = []
        
        event_reviews = reviews_db.get_reviews_by_eventId(eventId)
        if (len(event_reviews) > 0):
            review_list = []
            for review in event_reviews:
                review_list.append({"reviewedBy":reviews_db.get_username_from_id(review['userId']),
                                    "reviewedByUserId":review['userId'],
                                    "review":review['review'],
                                    "reviewedOn":review['reviewTimeStamp'],
                                    "rating":review['rating'],
                                    "reply":review['reply'],
                                    "repliedOn":review['replyTimeStamp']
                                    })
                #event_list.append([event['id']])
            result_dict['reviews'] = review_list
        
        return {
            'resultStatus': 'SUCCESS',
            'message': result_dict
        }
    
    def post(self):
        # parse request
        getRequest = request.json
        if ('token' in getRequest):
            token = getRequest['token']
        else:
            return {"status": "Error", "message": "token was not Sent"}
        
        if ('eventId' in getRequest):
            eventId = getRequest['eventId']
        else:
            return {"status": "Error", "message": "Event Id was not Sent"}
        
        if ('timeStamp' in getRequest):
            timeStamp = getRequest['timeStamp']
        else:
            return {"status": "Error", "message": "Time Stamp was not Sent"}
        
        if ('comment' in getRequest):
            comment = getRequest['comment']
        else:
            comment = ""
        
        if ('rating' in getRequest):
            rating = getRequest['rating']
        
        
        # create db engine
        token_db = TokenHandlerDB()
        reviews_db = ReviewsDB()
        
        # check user exists
        user_exists = token_db.check_usertoken_exists(token)
        
        if user_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User Token does not match'
            }
        
        user_id = token_db.get_host_id_from_token(token)
        
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
        
        new_id = reviews_db.post_review(user_id, eventId, timeStamp, comment, rating, host, eventType)
        
        if new_id == -1:
            return {"status": "Error", "message": "Could not add review"}
        else:
            return {"status": "Success", "message": "Added Review Succesfully"}
        
    
    def patch(self):
        # parse request
        getRequest = request.json
        if ('token' in getRequest):
            token = getRequest['token']
        else:
            return {"status": "Error", "message": "token was not Sent"}
        
        if ('eventId' in getRequest):
            eventId = getRequest['eventId']
        else:
            return {"status": "Error", "message": "Event Id was not Sent"}
        
        user_reviews_params = {}
        
        if ('timeStamp' in getRequest):
            reviewedTime = datetime.datetime.strptime(getRequest['timeStamp'], '%Y-%m-%d %H:%M')
            user_reviews_params['reviewTimeStamp'] = reviewedTime
        
        if ('comment' in getRequest):
            user_reviews_params['review'] = getRequest['comment']
        
        if ('rating' in getRequest):
            user_reviews_params['rating'] = getRequest['rating']
        
        # create db engine
        token_db = TokenHandlerDB()
        reviews_db = ReviewsDB()
        
        # check user exists
        user_exists = token_db.check_usertoken_exists(token)
        
        if user_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User Token does not match'
            }
        
        user_id = token_db.get_host_id_from_token(token)
        
        user_has_reviewed = reviews_db.check_user_hasComment(user_id, eventId)
        
        if user_has_reviewed == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User has not reviewed before'
            }
        
        
        new_id = reviews_db.update_user_reviews(user_reviews_params, user_id, eventId)
        
        if new_id == -1:
            return {"status": "Error", "message": "Could not update review!"}
        else:
            return {"status": "Success", "message": "Updated Review Succesfully"}
    
    def delete(self):
        # parse request
        getRequest = request.json
        if ('token' in getRequest):
            token = getRequest['token']
        else:
            return {"status": "Error", "message": "token was not Sent"}
        
        if ('eventId' in getRequest):
            eventId = getRequest['eventId']
        else:
            return {"status": "Error", "message": "Event Id was not Sent"}
        
        # create db engine
        token_db = TokenHandlerDB()
        reviews_db = ReviewsDB()
        
        # check user exists
        user_exists = token_db.check_usertoken_exists(token)
        
        if user_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User Token does not match'
            }
        
        user_id = token_db.get_host_id_from_token(token)
        
        user_has_reviewed = reviews_db.check_user_hasComment(user_id, eventId)
        
        if user_has_reviewed == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User has not reviewed before!'
            }
        
        new_id = reviews_db.delete_user_reviews(user_id, eventId)
        
        if new_id == -1:
            return {"status": "Error", "message": "Could not delete review"}
        else:
            return {"status": "Success", "message": "Deleted Review Succesfully"}