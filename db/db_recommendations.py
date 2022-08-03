# import third party libaries
from sqlalchemy.exc import IntegrityError
import sqlalchemy as db
from sqlalchemy import and_
from datetime import date


class RecommendationsDB:
    def __init__(self):
        from app import databaseTables

        self.temp_db = databaseTables

    def get_eventid_with_tickets(self, userId):
        event_ticket_query = db.select([self.temp_db.tickets]).where(self.temp_db.tickets.c.user_id == userId)
        eventid_with_tickets = set()
        
        try:
            result = self.temp_db.engine.execute(event_ticket_query)
            result = ({'result': [dict(row) for row in result]})
            
            for i in range(len(result['result'])):
                eventid_with_tickets.add(result["result"][i]['event_id'])
            
            return eventid_with_tickets
        except IntegrityError as e:
            return (400, "could not find review for event") 

    def get_recommend_event_bytype(self, eventTypes):
        return_ids = set()
        today = date.today();
        query = db.select([self.temp_db.events]).where(
            and_(
                self.temp_db.events.c.type.in_(tuple(eventTypes)),
                self.temp_db.events.c.start_date > today,
                self.temp_db.events.c.deleted == False
                )
            )
        try:
            result = self.temp_db.engine.execute(query)
            result = ({'result': [dict(row) for row in result]})
            for i in range(len(result['result'])):
                return_ids.add(result["result"][i]['id'])
                
            return return_ids
        except IntegrityError as e:
            return (400, "could not find event")

    def get_recommend_event_byhost(self, eventHosts):
        # This functions searches for events with event_name as event_name and returns a list of all events
        #datetime.datetime.strptime(row.start_date, "%d-%m-%Y").date()
        today = date.today();
        return_ids = set()
        query = db.select([self.temp_db.events]).where(
            and_(
                self.temp_db.events.c.host_username.in_(tuple(eventHosts)),
                self.temp_db.events.c.start_date > today,
                self.temp_db.events.c.deleted == False
                )
            )
        try:
            result = self.temp_db.engine.execute(query)
            result = ({'result': [dict(row) for row in result]})
            for i in range(len(result['result'])):
                return_ids.add(result["result"][i]['id'])
                
            return return_ids
        except IntegrityError as e:
            return (400, "could not find event")

    def get_future_events(self):
        today = date.today();
        query = db.select([self.temp_db.events]).where(
            and_(
                self.temp_db.events.c.start_date > today,
                self.temp_db.events.c.deleted == False
                )
            )
        try:
            result = self.temp_db.engine.execute(query)
            result = ({'result': [dict(row) for row in result]})
            for i in range(len(result['result'])):
                result["result"][i]['start_date'] = str(result["result"][i]['start_date'])
                result["result"][i]['start_time'] = str(result["result"][i]['start_time'])
                result["result"][i]['end_date'] = str(result["result"][i]['end_date'])
                result["result"][i]['end_time'] = str(result["result"][i]['end_time'])
                
            return result["result"]
        except IntegrityError as e:
            return (400, "could not find event")