'''
Written by: Group 404
For COMP9900 Project 7 Event Management System

This file defines the Resources that connect the front end URLs to the backend which will call the database.

'''

from flask_restful import Api, Resource, reqparse
from flask import request
from db.init_db import InitDB

class SignUp(Resource):
    def get(self):
        return {
            'resultStatus': 'SUCCESS',
            'message': "Hello This is Sign Up response"
        }

    def post(self): 
        print("0")
        print(request.json)
        print("0.5")
        data = request.get_json()
        print(data)
        print(self)
        print("1")
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str)
        parser.add_argument('message', type=str)
        print("2")
        args = parser.parse_args()
        print("2.4")
        print(args)
        print("3")
        # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')

        request_type = args['type']
        request_json = args['message']
        print("4")
        # ret_status, ret_msg = ReturnData(request_type, request_json)
        # currently just returning the req straight
        ret_status = request_type
        ret_msg = request_json
        print("5")
        if ret_msg:
            message = "Your Message Requested: {}".format(ret_msg)
        else:
            message = "No Msg"
        
        final_ret = {"status": "Success", "message": message}

        return final_ret

class ApiHandler(Resource):
    def get(self):
        return {
            'resultStatus': 'SUCCESS',
            'message': "Hello Api Handler"
        }

    def post(self):
        print(self)
        parser = reqparse.RequestParser()
        parser.add_argument("type", type=str)
        parser.add_argument("message", type=str)
        print("a")
        args = parser.parse_args()
        print("b")
        print(args)
        # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')
        print("c")
        request_type = args['type']
        request_json = args['message']
        # ret_status, ret_msg = ReturnData(request_type, request_json)
        # currently just returning the req straight
        ret_status = request_type
        ret_msg = request_json

        if ret_msg:
            message = "Your Message Requested: {}".format(ret_msg)
        else:
            message = "No Msg"
    
        final_ret = {"status": "Success", "message": message}

        return final_ret

class Events(Resource):
    def get(self):
        temp_db = InitDB()
        result = temp_db.select_all_events()

        return {
            'resultStatus': 'SUCCESS',
            'message': result
        }

class Login(Resource):
    def post(self):
        temp_db = InitDB()
        result = temp_db.user_check_exists()


        return {
            'resultStatus': 'SUCCESS',
            'message': result
        }