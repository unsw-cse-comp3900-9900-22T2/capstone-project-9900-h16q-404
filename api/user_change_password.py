"""
Written by: Group 404

This file handles the API requests for editing user login information

"""
# import third party libraries
from flask_restful import Resource
from flask import request

# import custom classes used to interact with the DB
from db.db_token_handler import TokenHandlerDB
from db.db_users import UsersDB


class UserChangePassword(Resource):
    def patch(self):

        # parse request
        getRequest = request.json
        if "token" in getRequest:
            user_token = request.json["token"]
        else:
            return {"status": "Error", "message": "User Token was not Sent"}

        # create db engines
        token_db = TokenHandlerDB()
        users_db = UsersDB()

        user_exists = token_db.check_usertoken_exists(user_token)

        if user_exists == False:
            return {"status": "Error", "message": "User does not exists"}

        if "old_password" in getRequest:
            old_password = request.json["old_password"]
        else:
            return {"status": "Error", "message": "User Old Password was not Sent"}

        password_match = users_db.check_passwords_match(user_token, old_password)
        if password_match == False:
            return {"status": "Error", "message": "Old password is not correct"}

        user_details_params = {}

        if "new_email" in getRequest:
            user_details_params["email"] = request.json["new_email"]

        if "new_password" in getRequest:
            user_details_params["password"] = request.json["new_password"]

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
            "message": "User Password Successfully Reset!",
        }
