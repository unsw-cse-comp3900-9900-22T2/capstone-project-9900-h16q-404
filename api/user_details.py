'''
Written by: Group 404

This file handles the API requests for editing user details

'''

from flask_restful import Resource
from db.init_db import InitDB
from flask import request


class UserDetails(Resource):
    def patch(self):
        temp_db = InitDB()
        getRequest = request.json
        if ('token' in getRequest):
            user_token = request.json['token']
        else:
            return {"status": "Error", "message": "User Token was not Sent"}
        
        user_exists = temp_db.check_usertoken_exists(user_token)
        
        if (user_exists == False):
            return {"status": "Error", "message": "User does not exists"}
        
        user_details_params = {}
        
        if ('firstName' in getRequest):
            user_details_params['firstName'] = request.json['firstName']
        
        if ('lastName' in getRequest):
            user_details_params['lastName'] = request.json['lastName']
        
        if ('phone' in getRequest):
            user_details_params['phone'] = request.json['phone']
        
        if user_details_params:
            update_status = temp_db.update_user_details(user_details_params, user_token)
        else:
            update_status = 0
        
        if (update_status == -1):
            return {"status": "Error", "message": "Update Failed! Try Again!"}
        
        return {
            'resultStatus': 'SUCCESS',
            'message': "User Details Updated!"
        }