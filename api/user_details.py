"""
Written by: Group 404

This file handles the API requests for editing user details

"""
# import third party libraries
from flask_restful import Resource
from flask import request

# import custom classes used to interact with the DB
from db.db_users import UsersDB
from db.db_token_handler import TokenHandlerDB


class UserDetails(Resource):
    def patch(self):

        # parse request
        getRequest = request.json
        if "token" in getRequest:
            user_token = request.json["token"]
        else:
            return {"status": "Error", "message": "User Token was not Sent"}

        # create db engines
        users_db = UsersDB()
        token_db = TokenHandlerDB()

        user_exists = token_db.check_usertoken_exists(user_token)

        if user_exists == False:
            return {"status": "Error", "message": "User does not exists"}

        user_details_params = {}

        if "firstName" in getRequest:
            user_details_params["firstName"] = request.json["firstName"]

        if "lastName" in getRequest:
            user_details_params["lastName"] = request.json["lastName"]

        if "phone" in getRequest:
            user_details_params["phone"] = request.json["phone"]
        
        if "image" in getRequest:
            user_details_params["image"] = request.json["image"]

        if user_details_params:
            update_status = users_db.update_user_details(
                user_details_params, user_token
            )
        else:
            update_status = 0

        if update_status == -1:
            return {"status": "Error", "message": "Update Failed! Try Again!"}

        return {
            "resultStatus": "SUCCESS",
            "message": "User Details Updated!",
        }
