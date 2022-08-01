"""
Written by: Group 404

This file handles all API requests for registering a user

"""
# import third party libaries
from flask_restful import Resource, reqparse

# import custom classes used to interact with the DB
from db.db_users import UsersDB


class Register(Resource):
    def post(self): 

        # parse request
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str)
        parser.add_argument("confirm", type=str)
        args = parser.parse_args()

        request_email = args["email"]
        request_password = args["password"]

        # create db engines
        user_db = UsersDB()

        # check user exists
        user_exists = user_db.check_user_exists(request_email)

        # if user does not exists return error
        if user_exists == True:
            return {"status": "Error", "message": "User already exists"}

        # if user does not exists, store password and username
        new_id = user_db.register_new_user(request_email, request_password)

        if new_id == -1:
            return {"status": "Error", "message": "could not register new user"}
        else:
            final_ret = {
                "status": "Success", 
                "message": "new user registerd with id = " +str(new_id)
            }

        return final_ret
