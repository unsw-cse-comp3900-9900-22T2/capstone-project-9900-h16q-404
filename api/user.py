"""
Written by: Group 404

This file handles the API requests for visting a user page and returning user information

"""
# import third party libraries
from flask_restful import Resource, reqparse

# import custom classes used to interact with the DB
from db.db_users import UsersDB
from db.db_events import EventsDB


class User(Resource):
    def get(self):

        # parse request
        parser = reqparse.RequestParser()
        parser.add_argument("userId", type=int, location="args")
        args = parser.parse_args()

        request_userId = args["userId"]

        # create db engines
        user_db = UsersDB()
        events_db = EventsDB()

        user_exists = user_db.check_userid_exists(request_userId)

        if user_exists is False:
            return {"status": "Error", "message": "User does not exists"}

        user_record = user_db.get_user_record(request_userId)
        result_dict = {}
        result_dict["userId"] = user_record[0][0]
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

        # Get events hosted by this user
        result_dict["events"] = []
        user_events = events_db.select_events_hostid(request_userId)

        if len(user_events) > 0:
            event_list = []
            for event in user_events:
                event_list.append(
                    {
                        "id": event["id"],
                        "name": event["event_name"],
                        "startDate": event["start_date"],
                    }
                )
            result_dict["events"] = event_list

        return {"resultStatus": "SUCCESS", "message": result_dict}
