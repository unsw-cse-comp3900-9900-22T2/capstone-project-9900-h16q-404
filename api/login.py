"""
Written by: Group 404

This file handles the API requests for logging in a user 

"""
# import third party libraries
from flask_restful import Resource, reqparse

# import custom classes used to interact with the DB
from db.db_users import UsersDB


class Login(Resource):
    def post(self):

        # parse request
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)
        args = parser.parse_args()

        request_username = args["username"]
        request_password = args["password"]

        # create db engines
        users_db = UsersDB()

        user_exists = users_db.check_user_exists(request_username)

        if user_exists == False:
            return {"status": "Error", "message": "User does not exists"}

        # if user does exist, check passwords match
        if user_exists == True:
            passwords_match = users_db.check_passwords_match(
                request_username, request_password
            )

        if passwords_match == False:
            return {"status": "Error", "message": "Password is incorrect"}

        user_record = users_db.get_user_record_byname(request_username)
        result_dict = {}
        result_dict["userId"] = user_record[0][0]
        result_dict["token"] = user_record[0][3]
        result_dict["email"] = user_record[0][4]
        result_dict["firstname"] = user_record[0][5]
        result_dict["lastname"] = user_record[0][6]

        # check dob not none then convert to string
        dob = user_record[0][7]
        result_dict["dateOfBirth"] = dob
        if dob is not None:
            result_dict["dateOfBirth"] = dob.strftime("%Y-%m-%d")

        result_dict["gender"] = user_record[0][8]
        result_dict["phone"] = user_record[0][9]
        result_dict["vac"] = user_record[0][10]

        return {"resultStatus": "SUCCESS", "message": result_dict}
