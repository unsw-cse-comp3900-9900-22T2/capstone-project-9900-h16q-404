'''
Written by: Group 404

This file handles the API requests for editing user login information

'''

from flask_restful import Resource
from db.init_db import InitDB
from flask import request


class UserChangePassword(Resource):
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

        # Yunran: Please include check old password here
        if ('old_password' in getRequest):
            old_password = request.json['old_password']
        else:
            return {"status": "Error", "message": "User Old Password was not Sent"}
        
        password_match = temp_db.check_passwords_match(user_token, old_password)
        if password_match == False:
            return {"status": "Error", "message": "Old password is not correct"}
        # Yunran: TODO: Please include update email here; can update email only or password only
        
        user_details_params = {}
        
        if ('new_email' in getRequest):
            user_details_params['email'] = request.json['new_email']
        
        if ('new_password' in getRequest):
            user_details_params['password'] = request.json['new_password']
        
        if user_details_params:
            update_status = temp_db.update_user_details(user_details_params, user_token)
        else:
            update_status = 0
        
        if (update_status == -1):
            return {"status": "Error", "message": "Update Failed! Try Again!"}
        
        return {
            'resultStatus': 'SUCCESS',
            'message': "User Password Successfully Reset!"
        }