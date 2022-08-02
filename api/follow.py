"""
Written by: Group 404

This file handles the API requests for following and unfollowing users

"""

from db.db_follow import FollowDB
from db.db_token_handler import TokenHandlerDB

from flask_restful import Resource, reqparse


class Follow(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        parser.add_argument('target_id', type=str, location='args')
        args = parser.parse_args()
        
        # assign variables
        token = args['token']
        following_id = args['target_id']

        follow_db = FollowDB()
        token_db = TokenHandlerDB()

        follower_id = token_db.get_host_id_from_token(token)
        return follow_db.check_follower(follower_id, following_id)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        parser.add_argument('target_id', type=str)
        args = parser.parse_args()
        
        # assign variables
        token = args['token']
        following_id = args['target_id']

        follow_db = FollowDB()
        token_db = TokenHandlerDB()

        follower_id = token_db.get_host_id_from_token(token)

        return follow_db.add_follower(follower_id, following_id)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        parser.add_argument('target_id', type=str)
        args = parser.parse_args()
        
        # assign variables
        token = args['token']
        following_id = args['target_id']

        follow_db = FollowDB()
        token_db = TokenHandlerDB()

        follower_id = token_db.get_host_id_from_token(token)

        return follow_db.delete_follower(follower_id, following_id)