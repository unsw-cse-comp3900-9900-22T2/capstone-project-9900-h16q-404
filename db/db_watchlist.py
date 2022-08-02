

import sqlalchemy as db


class WatchlistDB:
    def __init__(self):
        from app import databaseTables

        self.temp_db = databaseTables

    def get_all_following_user_ids(self, user_id):

        check_follower_query = db.select([self.temp_db.watchlist]).where(self.temp_db.watchlist.c.follower == user_id)
        result = self.temp_db.engine.execute(check_follower_query)
        result = {'result': [dict(row) for row in result]}
        return result['result']