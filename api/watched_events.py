

from db.db_token_handler import TokenHandlerDB
from db.db_watchlist import WatchlistDB
from db.db_events import EventsDB

# import third party libraries
from flask_restful import Resource, reqparse

class WatchedEvents(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        args = parser.parse_args()
        
        # assign variables
        token = args['token']

        token_db = TokenHandlerDB()
        watchlist_db = WatchlistDB()
        events_db = EventsDB()

        user_id = token_db.get_host_id_from_token(token)

        following_users = watchlist_db.get_all_following_user_ids(user_id)
        
        return_events = []
        for i in following_users:
            events = events_db.select_events_hostid(i['following'])
            for j in events:
                return_events.append(j)

        return return_events