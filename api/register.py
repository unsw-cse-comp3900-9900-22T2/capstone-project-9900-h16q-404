'''
Written by: Group 404

This file handles all API requests for registering a user

'''

from flask_restful import Resource, reqparse
from db.init_db import InitDB


class Register(Resource):
    def get(self):
        return {
            'resultStatus': 'SUCCESS',
            'message': "Hello This is Sign Up response"
        }

    def post(self): 
        # If a post request is sent to /register

        # parse request
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('confirm', type=str)
        args = parser.parse_args()

        # get email and password
        request_email = args['email']
        request_password = args['password']

        temp_db = InitDB()
        # check user exists
        user_exists = temp_db.check_user_exists(request_email)

        # if user does not exists return error
        if user_exists == True:
            return {"status": "Error", "message": "User already exists"}
            

        # TODO here:
        # if user does not exists, store password and username
        new_id = temp_db.register_new_user(request_email, request_password)
        if new_id == -1:
            return {"status": "Error", "message": "could not register new user"}
        else:
            final_ret = {"status": "Success", "message": "new user registerd with id = " +str(new_id)}

        return final_ret