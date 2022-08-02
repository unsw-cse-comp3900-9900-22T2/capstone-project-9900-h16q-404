
import sqlalchemy as db
from sqlalchemy import and_


class FollowDB:
    def __init__(self):
        from app import databaseTables

        self.temp_db = databaseTables

    def check_follower(self, follower_id, following_id):
        
        check_follower_query = db.select([self.temp_db.watchlist]).where(
            and_(
                self.temp_db.watchlist.c.follower == follower_id,
                self.temp_db.watchlist.c.following == following_id
                )
            )
        result = self.temp_db.engine.execute(check_follower_query)
        result = ({'result': [dict(row) for row in result]})

        if len(result['result']) > 0:
            return True
        else:
            return False

    def add_follower(self, follower_id, following_id):

        if self.check_follower(follower_id, following_id) == False:

            try:
                query = db.insert(self.temp_db.watchlist).values(
                        id = self.temp_db.get_max_watchlist_id(),
                        follower = follower_id,
                        following = following_id
                    )
                self.temp_db.engine.execute(query).inserted_primary_key
                return "Success: Added to watchlist"
            except:
                print(6)
                return "ERROR: Could not add to watchlist"
        else:
            return "ERROR: Already a follower"

    def delete_follower(self, follower_id, following_id):

        if self.check_follower(follower_id, following_id) == True:
            try:
                delete_follower_query = db.delete(self.temp_db.watchlist).where(
                    and_(
                        self.temp_db.watchlist.c.follower == follower_id,
                        self.temp_db.watchlist.c.following == following_id
                    )
                )
                result = self.temp_db.engine.execute(delete_follower_query)
                return "Success"
            except:
                return "ERROR: Could not remove from watchlist"
        else:
            return "ERROR: You do not follow this user"

    def get_all_following_user_ids(self, user_id):

        check_follower_query = db.select([self.temp_db.watchlist]).where(self.temp_db.watchlist.c.follower == user_id)
        result = self.temp_db.engine.execute(check_follower_query)
        result = ({'result': [dict(row) for row in result]}) 
        return result['result']

    def get_max_watchlist_id(self):
        # returns the highest id in the tickets table plus 1
        query_max_id = db.select([db.func.max(self.watchlist.columns.id)])
        max_id = self.engine.execute(query_max_id).scalar()
        if max_id == None:
            max_id = 0
        return max_id + 1