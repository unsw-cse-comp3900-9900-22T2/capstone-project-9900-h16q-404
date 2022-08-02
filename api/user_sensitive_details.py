"""
Written by: Group 404

This file handles the API requests for editing sensitive user details

"""
# import third party libraries
from flask_restful import Resource
from flask import request
from datetime import datetime

# import custom classes used to interact with the DB
from db.db_users import UsersDB
from db.db_token_handler import TokenHandlerDB


class UserSensitiveDetails(Resource):
    def patch(self):

        # parse request
        getRequest = request.json
        if ("token" in getRequest):
            user_token = request.json["token"]
        else:
            return {"status": "Error", "message": "User Token was not Sent"}

        # create db engines
        token_db = TokenHandlerDB()
        user_db = UsersDB()
            
        user_exists = token_db.check_usertoken_exists(user_token)
        
        if (user_exists == False):
            return {"status": "Error", "message": "User does not exists"}
        
        user_details_params = {}
        
        if ("dateOfBirth" in getRequest):
            dob = datetime.strptime(request.json["dateOfBirth"], "%Y-%m-%d")
            user_details_params["dateOfBirth"] = dob
        
        if ("gender" in getRequest):
            user_details_params["gender"] = request.json["gender"]
        
        if ("vaccinated" in getRequest):
            user_details_params["vaccinated"] = request.json["vaccinated"]
        
        if user_details_params:
            update_status = user_db.update_user_details(user_details_params, user_token)
        else:
            update_status = 0
        
        if (update_status == -1):
            return {"status": "Error", "message": "Update Failed! Try Again!"}
        
        return {
            "resultStatus": "SUCCESS",
            "message": "Sensitive Details Updated!"
        }