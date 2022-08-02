

# import third party libaries
from sqlalchemy.exc import IntegrityError
import sqlalchemy as db


class UserRatingsDB:
    def __init__(self):
        from app import databaseTables

        self.temp_db = databaseTables


    def select_ratings_by_host(self, host):
        rating_host_query = db.select([self.temp_db.reviews]).where(self.temp_db.reviews.c.host == host)
        
        try:
            result = self.temp_db.engine.execute(rating_host_query)
            result = ({'result': [dict(row) for row in result]})
            for i in range(len(result['result'])):
                result["result"][i]['reviewTimeStamp'] = str(result["result"][i]['reviewTimeStamp'])
                result["result"][i]['replyTimeStamp'] = str(result["result"][i]['replyTimeStamp'])
                
            return result["result"]
        except IntegrityError as e:
            return (400, "could not find review for event")