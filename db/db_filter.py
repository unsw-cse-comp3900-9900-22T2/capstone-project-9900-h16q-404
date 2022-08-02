"""
Functions:
# get/select
- select_events_bytype
# create/insert
# update
# delete
# helper
"""

# import third party libaries
import logging
import sqlalchemy as db
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)


class FilterDB:
    def __init__(self):
        from app import databaseTables

        self.temp_db = databaseTables

    # Functions for selecting/getting events

    def select_events_bytype(self, type):
        query = db.select([self.temp_db.events]).where(
            and_(
                self.temp_db.events.c.type == type,
                self.temp_db.events.c.deleted == False,
            )
        )
        try:
            result = self.temp_db.engine.execute(query)
            result = {"result": [dict(row) for row in result]}
            for i in range(len(result["result"])):
                result["result"][i]["start_date"] = str(
                    result["result"][i]["start_date"]
                )
                result["result"][i]["start_time"] = str(
                    result["result"][i]["start_time"]
                )
                result["result"][i]["end_date"] = str(result["result"][i]["end_date"])
                result["result"][i]["end_time"] = str(result["result"][i]["end_time"])

            return result["result"]
        except IntegrityError as e:
            logger.exception(e)
            return (400, "could not find event")
