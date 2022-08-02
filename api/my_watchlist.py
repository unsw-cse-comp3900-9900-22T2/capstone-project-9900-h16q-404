"""
Written by: Group 404

This file handles the API requests for getting, editing and deleting event information

"""

from db.db_watchlist import WatchlistDB
from db.db_users import UsersDB
from db.db_token_handler import TokenHandlerDB

# import third party libraries
from flask_restful import Resource, reqparse


class MyWatchlist(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        args = parser.parse_args()
        
        # assign variables
        token = args['token']

        token_db = TokenHandlerDB()
        watchlist_db = WatchlistDB()
        users_db = UsersDB()

        user_id = token_db.get_host_id_from_token(token)

        all_following_ids = watchlist_db.get_all_following_user_ids(user_id)
        
        all_following_user_details = []

        for i in all_following_ids:
            user_record = users_db.get_user_record(i['following'])
            if user_record != -1:
                all_following_user_details.append(user_record[0])

        return_users = []
        for i in all_following_user_details:
            user_dict = {}
            user_dict['user_id'] = i[0]
            user_dict['user_name'] = i[1]
            return_users.append(user_dict)

        return return_users