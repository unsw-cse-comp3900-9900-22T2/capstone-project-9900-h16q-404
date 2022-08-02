


# import third party libaries
from sqlalchemy.exc import IntegrityError
import sqlalchemy as db
from sqlalchemy import and_
import datetime


class EventRatingsDB:
    def __init__(self):
        from app import databaseTables

        self.temp_db = databaseTables

    def select_ratings_from_reviews(self, host, eventType):
        review_rating_query = db.select([self.temp_db.reviews]).where(
            and_(
                self.temp_db.reviews.c.host == host,
                self.temp_db.reviews.c.eventType == eventType
                )
            )
        
        try:
            result = self.temp_db.engine.execute(review_rating_query)
            result = ({'result': [dict(row) for row in result]})
            for i in range(len(result['result'])):
                result["result"][i]['reviewTimeStamp'] = str(result["result"][i]['reviewTimeStamp'])
                result["result"][i]['replyTimeStamp'] = str(result["result"][i]['replyTimeStamp'])
                
            return result["result"]
        except IntegrityError as e:
            return (400, "could not find review for event")