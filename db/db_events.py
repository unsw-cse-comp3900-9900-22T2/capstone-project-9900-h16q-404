'''
Functions:
# get
- select_event_id
- select_all_events
# create
- create_event
- insert_events
# update
- update_event
# delete
- delete_event_id
- delete_event_name
# helper
- get_new_event_id
- check_event_exists
- get_event_time_date
- select_events_hostid
- flatten_details
'''


# import third party libraries
import sqlalchemy as db
from sqlalchemy import and_
import datetime
from sqlalchemy.exc import IntegrityError
import pandas as pd

# import custom classes used to interact with the DB
from db.db_tickets import TicketsDB
from db.db_token_handler import TokenHandlerDB

class EventsDB:
    def __init__(self):
        from app import databaseTables
        self.temp_db = databaseTables


# Functions for selecting/getting event info

    def select_event_id(self, event_id):
        # This functions searches for events with id as event_id and returns a list of all events
        query = db.select([self.temp_db.events]).where(self.temp_db.events.c.id == event_id)
        try:
            result = self.temp_db.engine.execute(query)
            result = ({'result': [dict(row) for row in result]})
            for i in range(len(result['result'])):
                result["result"][i]['start_date'] = str(result["result"][i]['start_date'])
                result["result"][i]['start_time'] = str(result["result"][i]['start_time'])[:-3]
                result["result"][i]['end_date'] = str(result["result"][i]['end_date'])
                result["result"][i]['end_time'] = str(result["result"][i]['end_time'])[:-3]
            return result["result"]
        except IntegrityError as e:
            return (400, "could not find event")

    def select_events_hostid(self, host_id):
        # This functions searches for events with event_name as event_name and returns a list of all events
        query = db.select([self.temp_db.events]).where(
            and_(
                self.temp_db.events.c.host == host_id,
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

    def select_all_events(self):
        # This funtion currently returns a list of all the rows of the events table
        query = db.select([self.temp_db.events]).where(self.temp_db.events.c.deleted == False)
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
            return (400, "Could not select from table")

# Functions for creating/inserting events into table

    def create_event(self, token, event_details):
        # This function takes a token and a nested dictionary of event details, it flattens 
        # the dict, finds a new ID for the new event, gets the host ID and username from the
        # token, formats all of the data required for the insertion into the event table and 
        # finally returns the event details and event ID

        event_details = self.flatten_details(event_details)
        new_id = self.get_new_event_id()
        
        token_db = TokenHandlerDB()
        
        host = token_db.get_host_id_from_token(token)
        host_username = token_db.get_host_username_from_token(token)

        insert_data = {}
        insert_data['id'] = new_id
        insert_data['event_name'] = event_details['title']
        insert_data['type'] = event_details['type']
        insert_data['location'] = event_details['location']
        insert_data['host'] = host
        insert_data['host_username'] = host_username
        insert_data['deleted'] = False 
        insert_data['description'] = event_details['desc']
        insert_data['adult_only'] = event_details['cond_adult']
        insert_data['vax_only'] = event_details['cond_vax'] 
        insert_data['start_date'] = datetime.datetime.strptime(event_details['startdate'], "%Y-%m-%d").date()
        insert_data['start_time'] = datetime.datetime.strptime( event_details['starttime'], "%H:%M").time()
        insert_data['end_date'] = datetime.datetime.strptime(event_details['enddate'], "%Y-%m-%d").date()
        insert_data['end_time'] = datetime.datetime.strptime( event_details['endtime'], "%H:%M").time()
        insert_data['gold_num'] = event_details['gold_num']
        insert_data['gold_price'] = event_details['gold_price']
        insert_data['silver_num'] = event_details['silver_num']
        insert_data['silver_price'] = event_details['silver_price']
        insert_data['bronze_num'] = event_details['bronze_num']
        insert_data['bronze_price'] = event_details['bronze_price']

        result = self.insert_events(insert_data), insert_data
        
        return result

    def insert_events(self, data):
        # This function takes a JSON object "data" and inserts the object into the DB as a new row
        # But first the function checks if a row with the same ID aleady exists
        
        # check for row with existing primary key
        insert_check = True
        check_query = db.select([self.temp_db.events]).where(self.temp_db.events.c.id == data["id"])
        check_result = self.temp_db.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})

        for i in range(len(check_result['result'])):
             if data["id"] == (check_result["result"][i]['id']):
                insert_check = False

        tickets_db = TicketsDB()

        # if no row exists with current primary key add new row
        if insert_check == True:
            query = db.insert(self.temp_db.events).values(
                id = data["id"],
                event_name = data["event_name"],
                host = data["host"],
                host_username = data['host_username'],
                type = data["type"],
                start_date = data["start_date"],
                start_time = data["start_time"],
                end_date = data["end_date"],
                end_time = data["end_time"],
                deleted = data["deleted"],
                location = data["location"],
                adult_only = data["adult_only"],
                vax_only = data["vax_only"],
                description = data["description"],
                gold_num = data["gold_num"],
                gold_price = data["gold_price"],
                silver_num = data["silver_num"],
                silver_price = data["silver_price"],
                bronze_num = data["bronze_num"],
                bronze_price = data["bronze_price"]
            )
            try:
                result = self.temp_db.engine.execute(query).inserted_primary_key 
                tickets_db.pre_fill_tickets(data)
                return result
            except:
                return -1
        else:
            print("Item " + str(data["event_name"]) + " not added to events table as it failed the insert check")

# Functions for updating events

    def update_event(self, event_id, event_details, token):

        token_db = TokenHandlerDB()

        event_details = self.flatten_details(event_details)
        host = token_db.get_host_id_from_token(token)
        host_username = token_db.get_host_username_from_token(token)

        update_data = {}
        update_data['event_name'] = event_details['title']
        update_data['type'] = event_details['type']
        update_data['location'] = event_details['location']
        update_data['host'] = host
        update_data['host_username'] = host_username
        update_data['deleted'] = False 
        update_data['description'] = event_details['desc']
        update_data['adult_only'] = event_details['cond_adult']
        update_data['vax_only'] = event_details['cond_vax'] 
        update_data['start_date'] = datetime.datetime.strptime(event_details['startdate'], "%Y-%m-%d").date()
        update_data['start_time'] = datetime.datetime.strptime( event_details['starttime'], "%H:%M").time()
        update_data['end_date'] = datetime.datetime.strptime(event_details['enddate'], "%Y-%m-%d").date()
        update_data['end_time'] = datetime.datetime.strptime( event_details['endtime'], "%H:%M").time()
        update_data['gold_num'] = event_details['gold_num']
        update_data['gold_price'] = event_details['gold_price']
        update_data['silver_num'] = event_details['silver_num']
        update_data['silver_price'] = event_details['silver_price']
        update_data['bronze_num'] = event_details['bronze_num']
        update_data['bronze_price'] = event_details['bronze_price']

        try:
            update_query = self.temp_db.events.update().values(update_data).where(self.temp_db.events.c.id == event_id)
            result = self.temp_db.engine.execute(update_query)
            return True
        except:
            return False

# Functions for deleting events

    def delete_event_id(self, event_id):
        if self.check_event_exists(event_id, "id"):
            try:
                query = self.temp_db.events.update().values(deleted=True).where(self.temp_db.events.c.id == event_id)
                result = self.temp_db.engine.execute(query)
                if result:
                    return (True)
            except IntegrityError as e:
                return ("Error updating delete column for " + event_id)

    def delete_event_name(self, event_name):
        if self.check_event_exists(event_name, "event_name"):
            try:
                query = self.temp_db.events.update().values(deleted=True).where(self.temp_db.events.c.event_name == event_name)
                result = self.temp_db.engine.execute(query)
                if result:
                    return (True)
            except IntegrityError as e:
                return (400, "Error updating delete column for " + event_name)
        else:
            return ("Error finding event " + event_name + " in events table")

# Helper functions

    def get_new_event_id(self):
        # returns the highest id in the user table plus 1
        query_max_id = db.select([db.func.max(self.temp_db.events.columns.id)])
        max_id = self.temp_db.engine.execute(query_max_id).scalar()
        return max_id + 1

    def check_event_exists(self, event_detail, event_col):
        event_exists = False

        if event_col == "id":
            check_query = db.select([self.temp_db.events]).where(self.temp_db.events.c.id == event_detail)
        else: 
            check_query = db.select([self.temp_db.events]).where(self.temp_db.events.c.event_name == event_detail)
        
        check_result = self.temp_db.engine.execute(check_query).fetchall()
        if len(check_result) > 0:
            event_exists = True
        return event_exists

    def get_event_time_date(self, event_id):
        event_start_query = db.select([self.temp_db.events]).where(self.temp_db.events.c.id == event_id)
        result = self.temp_db.engine.execute(event_start_query)
        result = ({'result': [dict(row) for row in result]})
        start_date = str(result['result'][0]['start_date'])
        start_time = str(result['result'][0]['start_time'])
        event_name = result['result'][0]['event_name']
        return start_date, start_time, event_name

    def flatten_details(self, data):
        return pd.json_normalize(data, sep='_').to_dict(orient='records')[0]