

# import third party libraries
from flask_restful import Resource
from flask import request
import datetime

from db.db_token_handler import TokenHandlerDB
from db.db_reviews import ReviewsDB

class HostReplies(Resource):
    def patch(self):
        getRequest = request.json
        if ('token' in getRequest):
            token = getRequest['token']
        else:
            return {"status": "Error", "message": "token was not Sent"}
            
        if ('eventId' in getRequest):
            eventId = getRequest['eventId']
        else:
            return {"status": "Error", "message": "Event Id was not Sent"}
        
        if ('targetUserId' in getRequest):
            targetUserId = getRequest['targetUserId']
        else:
            return {"status": "Error", "message": "Target User Id was not Sent"}
        
        host_replies_params = {}
        
        if ('timeStamp' in getRequest):
            repliedTime = datetime.datetime.strptime(getRequest['timeStamp'], '%Y-%m-%d %H:%M')
            host_replies_params['replyTimeStamp'] = repliedTime
        
        if ('reply' in getRequest):
            host_replies_params['reply'] = getRequest['reply']
        
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
        
        user_has_reviewed = reviews_db.check_user_hasComment(targetUserId, eventId)
        
        if user_has_reviewed == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User has not reviewed before'
            }
        
        new_id = reviews_db.update_user_reviews(host_replies_params, targetUserId, eventId)
        
        if new_id == -1:
            return {"status": "Error", "message": "Could not update reply!"}
        else:
            return {"status": "Success", "message": "Updated Reply Succesfully"}
        
    def delete(self):
        getRequest = request.json
        if ('token' in getRequest):
            token = getRequest['token']
        else:
            return {"status": "Error", "message": "token was not Sent"}
            
        if ('eventId' in getRequest):
            eventId = getRequest['eventId']
        else:
            return {"status": "Error", "message": "Event Id was not Sent"}
        
        if ('targetUserId' in getRequest):
            targetUserId = getRequest['targetUserId']
        else:
            return {"status": "Error", "message": "Target User Id was not Sent"}
        
        host_replies_delete_params = {}
        host_replies_delete_params['replyTimeStamp'] = None
        host_replies_delete_params['reply'] = ""
        
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
        
        user_has_reviewed = reviews_db.check_user_hasComment(targetUserId, eventId)
        
        if user_has_reviewed == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User has not reviewed before'
            }
        
        new_id = reviews_db.update_user_reviews(host_replies_delete_params, targetUserId, eventId)
        
        if new_id == -1:
            return {"status": "Error", "message": "Could not delete reply!"}
        else:
            return {"status": "Success", "message": "Deleted Reply Succesfully"}