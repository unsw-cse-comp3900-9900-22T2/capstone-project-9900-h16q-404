
from db.init_db import InitDB
import sqlalchemy as db
from sqlalchemy import and_
import json
import datetime
from db.db_token_handler import TokenHandlerDB
from db.db_tickets import TicketsDB

class EventsDB:
    def __init__(self):
        self.temp_db = InitDB()

    def create_event(self, token, event_details):
        # This function takes a token and a nested dictionary of event details, it flattens 
        # the dict, finds a new ID for the new event, gets the host ID and username from the
        # token, formats all of the data required for the insertion into the event table and 
        # finally returns the event details and event ID

        event_details = self.temp_db.flatten_details(event_details)
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

    def get_new_event_id(self):
        # returns the highest id in the user table plus 1
        query_max_id = db.select([db.func.max(self.temp_db.events.columns.id)])
        max_id = self.temp_db.engine.execute(query_max_id).scalar()
        return max_id + 1