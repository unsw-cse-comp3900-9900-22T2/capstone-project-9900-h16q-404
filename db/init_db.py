'''
Written by: Group 404
For COMP9900 Project 7 Event Management System

This file defines the InitDB class which currently contains all of the DB initialisation and 
querying functions

This file also has a main function, which when called creates an InitDB class and runs the 
fill_with_dummy_data function. This function reads dummy data from a csv and inserts it into 
the database.
'''

from asyncio import events
from requests import delete
from sqlalchemy.exc import IntegrityError
import sqlalchemy as db
from sqlalchemy import ForeignKey, null, select, and_, func
import pandas as pd
import datetime
from flask import jsonify
import json

# InitDB class
class InitDB:
    # This function is run upon creating an instance of the class
    def __init__(self):
        # create engine and connect to databse in the db folder
        self.engine = db.create_engine('sqlite:///db/group_404')
        # Metadata is a container object that kees together many of the different features fo a db
        self.metadata = db.MetaData()
        
        # Define the events tables
        self.events = db.Table('events', self.metadata,
            db.Column('id', db.Integer(), primary_key=True),
            db.Column('event_name', db.String(255), nullable=False),
            db.Column('host', db.Integer(), nullable=True),
            db.Column('host_username', db.String(255), nullable=True),
            db.Column('type', db.String(255), nullable=True),
            db.Column('start_date', db.Date, nullable=True),
            db.Column('start_time', db.Time, nullable=True),
            db.Column('end_date', db.Date, nullable=True),
            db.Column('end_time', db.Time, nullable=True),
            db.Column('deleted', db.Boolean, nullable=True),
            db.Column('location', db.String(255), nullable=True),
            db.Column('adult_only', db.Boolean, nullable=True),
            db.Column('vax_only', db.Boolean, nullable=True),
            db.Column('description', db.String(255), nullable=True),
            db.Column('gold_num', db.Integer(), nullable=True),
            db.Column('gold_price', db.Float(), nullable=True),
            db.Column('silver_num', db.Integer(), nullable=True),
            db.Column('silver_price', db.Float(), nullable=True),
            db.Column('bronze_num', db.Integer(), nullable=True),
            db.Column('bronze_price', db.Float(), nullable=True),
        )

        # define the users tables
        self.users = db.Table('users', self.metadata,
            db.Column('id', db.Integer(), primary_key=True),
            db.Column('username', db.String(255), nullable=True),
            db.Column('password', db.String(255), nullable=True),
            db.Column('token', db.String(255), nullable=True),
            db.Column('email', db.String(255), nullable=True),
            db.Column('firstName', db.String(255), nullable=True),
            db.Column('lastName', db.String(255), nullable=True),
            db.Column('dateOfBirth', db.Date, nullable=True),
            db.Column('gender', db.String(255), nullable=True),
            db.Column('phone', db.String(255), nullable=True),
            db.Column('vaccinated', db.Boolean(), nullable=True)
        )

        self.tickets = db.Table('tickets', self.metadata,
            db.Column('id', db.Integer(), primary_key=True),
            db.Column('event_id', db.Integer(), ForeignKey('events.id'), nullable=False),
            db.Column('user_id', db.Integer(), ForeignKey('users.id'), nullable=True),
            db.Column('seat_num', db.Integer(), nullable=False),
            db.Column('tix_class', db.String(10), nullable=False),
            db.Column('purchased', db.Boolean(), nullable=False),
            db.Column('card_number', db.Integer(), nullable=True),
            db.Column('ticket_price', db.String(16), nullable=False)
        )

        self.watchlist = db.Table('watchlist', self.metadata,
            db.Column('id', db.Integer(), primary_key=True),
            db.Column('follower', db.Integer(), ForeignKey('users.id'), nullable=False),
            db.Column('following', db.Integer(), ForeignKey('users.id'), nullable=False)
        )
        
        # create all objects in the metadata object
        self.metadata.create_all(self.engine, checkfirst=True)

    def fill_dummy_data(self):
        # This function will read one or more CSVs and then insert the data from those CSVs into the relevant tables
        
        # read in dummy data from CSVs
        dummy_events_df = pd.read_csv("db/dummy_events.csv")
        dummy_users_df = pd.read_csv("db/dummy_users.csv")

        # Iterate through events pandas DF and insert each row into table using insert function
        for index, row in dummy_events_df.iterrows():
            data = {
                "id":row.id, 
                "event_name": row.event_name,
                "host": row.host,
                "host_username": row.host_username,
                "type": row.type,
                "start_date": datetime.datetime.strptime(row.start_date, "%d-%m-%Y").date(),
                "start_time": datetime.datetime.strptime(row.start_time, "%H:%M").time(),
                "end_date": datetime.datetime.strptime(row.end_date, "%d-%m-%Y").date(),
                "end_time": datetime.datetime.strptime(row.end_time, "%H:%M").time(),
                "deleted": row.deleted,
                "location": row.location,
                "adult_only": row.adult_only,
                "vax_only": row.vax_only,
                "description": row.description,
                "gold_num": row.gold_num,
                "gold_price": row.gold_price,
                "silver_num": row.silver_num,
                "silver_price": row.silver_price,
                "bronze_num": row.bronze_num,
                "bronze_price": row.bronze_price,
            }
            result = self.insert_events(data)
            if result == None or result == -1:
                print(data["event_name"] + " Not Added")
            else:
                print("Added new event with ID = " + str(result))

        for index, row in dummy_users_df.iterrows():
            data = {
                "id":row.id, 
                "username": row.username,
                "password": row.password,
                "token": row.token,
                "email" : row.username,
                "firstName" : '',
                "lastName" : '',
                "dateOfBirth" : datetime.datetime.strptime(row.dob, '%Y-%m-%d').date(),
                "gender" : '',
                "phone" : '',
                "vaccinated" : row.vac
            }
            new_id = self.insert_users(data, True)

    def insert_users(self, data, dummy):
        
        # check for row with existing primary key    
        insert_bool = self.insert_check(data)
        
        # if no row exists with current primary key add new row
        if insert_bool == True:
            if dummy == True:
                query = db.insert(self.users).values([data])
            try:
                result = self.engine.execute(query).inserted_primary_key 
                return result 
            except:
                return -1
        else:
            print("Item " + str(data["username"]) + " not added to user table as it failed the insert check")

    def insert_events(self, data):
        # This function takes a JSON object "data" and inserts the object into the DB as a new row
        # But first the function checks if a row with the same ID aleady exists
        
        # check for row with existing primary key        
        insert_bool = self.insert_check(data)

        # if no row exists with current primary key add new row
        if insert_bool == True:
            query = db.insert(self.events).values(
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
                result = self.engine.execute(query).inserted_primary_key 
                self.pre_fill_tickets(data)
                return result
            except:
                return -1
        else:
            print("Item " + str(data["event_name"]) + " not added to events table as it failed the insert check")

    def pre_fill_tickets(self, data):
        self.insert_tix(data['gold_num'], 'gold', data['id'], data['gold_price'])
        self.insert_tix(data['silver_num'], 'silver', data['id'], data['silver_price'])
        self.insert_tix(data['bronze_num'], 'bronze', data['id'], data['bronze_price'])

    def insert_tix(self, num_tix, tix_class, event_ID, price):
        for i in range(num_tix):
            query = db.insert(self.tickets).values(
                id = self.get_max_ticket_id(),
                event_id = event_ID,
                tix_class = tix_class,
                seat_num = i,
                purchased = False,
                ticket_price = price
            )
            result = self.engine.execute(query).inserted_primary_key

    def get_max_ticket_id(self):
        # returns the highest id in the tickets table plus 1
        query_max_id = db.select([db.func.max(self.tickets.columns.id)])
        max_id = self.engine.execute(query_max_id).scalar()
        if max_id == None:
            max_id = 0
        return max_id + 1

    def select_all_tickets(self, user_id):
        user_tickets_query = db.select([self.tickets]).where(
            and_(
                self.tickets.c.user_id == user_id,
                self.tickets.c.purchased == True
                )
            )
        result = self.engine.execute(user_tickets_query)
        result = ({'result': [dict(row) for row in result]})
        return result

    def get_event_time_date(self, event_id):
        event_start_query = db.select([self.events]).where(self.events.c.id == event_id)
        result = self.engine.execute(event_start_query)
        result = ({'result': [dict(row) for row in result]})
        start_date = str(result['result'][0]['start_date'])
        start_time = str(result['result'][0]['start_time'])
        event_name = result['result'][0]['event_name']
        return start_date, start_time, event_name

    def get_max_watchlist_id(self):
        # returns the highest id in the tickets table plus 1
        query_max_id = db.select([db.func.max(self.watchlist.columns.id)])
        max_id = self.engine.execute(query_max_id).scalar()
        if max_id == None:
            max_id = 0
        return max_id + 1

    def check_follower(self, follower_id, following_id):
        
        check_follower_query = db.select([self.watchlist]).where(
            and_(
                self.watchlist.c.follower == follower_id,
                self.watchlist.c.following == following_id
                )
            )
        result = self.engine.execute(check_follower_query)
        result = ({'result': [dict(row) for row in result]})

        if len(result['result']) > 0:
            return True
        else:
            return False

    def add_follower(self, follower_id, following_id):

        if self.check_follower(follower_id, following_id) == False:
            try:
                query = db.insert(self.watchlist).values(
                        id = self.get_max_watchlist_id(),
                        follower = follower_id,
                        following = following_id
                    )
                result = self.engine.execute(query).inserted_primary_key 
                return "Success: Added to watchlist"
            except:
                return "ERROR: Could not add to watchlist"
        else:
            return "ERROR: Already a follower"

    def delete_follower(self, follower_id, following_id):

        if self.check_follower(follower_id, following_id) == True:
            try:
                delete_follower_query = db.delete(self.watchlist).where(
                    and_(
                        self.watchlist.c.follower == follower_id,
                        self.watchlist.c.following == following_id
                    )
                )
                result = self.engine.execute(delete_follower_query)
                return "Success"
            except:
                return "ERROR: Could not remove from watchlist"
        else:
            return "ERROR: You do not follow this user"

    def get_all_following_user_ids(self, user_id):

        check_follower_query = db.select([self.watchlist]).where(self.watchlist.c.follower == user_id)
        result = self.engine.execute(check_follower_query)
        result = ({'result': [dict(row) for row in result]}) 
        return result['result']

    def insert_check(self, data):

        check_query = db.select([self.users]).where(self.users.c.id == data["id"])
        check_result = self.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})

        insert_bool = True
        for i in range(len(check_result['result'])):
             if data["id"] == (check_result["result"][i]['id']):
                insert_bool = False
        return insert_bool

# The main function creates an InitDB class and then calls the fill_with_dummy_data method
def db_main():
    db = InitDB()
    db.fill_dummy_data()
    return db


    # def select_event_name(self, event_name):
    #     # This functions searches for events with event_name as event_name and returns a list of all events
    #     query = db.select([self.events]).where(self.events.c.event_name == event_name)
    #     try:
    #         result = self.engine.execute(query)
    #         result = ({'result': [dict(row) for row in result]})
    #         for i in range(len(result['result'])):
    #             result["result"][i]['event_date'] = str(result["result"][i]['event_date'])
    #         return result["result"]
    #     except IntegrityError as e:
    #         return (400, "could not find event")

    # def select_event_id(self, event_id):
    #     # This functions searches for events with id as event_id and returns a list of all events
    #     query = db.select([self.events]).where(self.events.c.id == event_id)
    #     try:
    #         result = self.engine.execute(query)
    #         result = ({'result': [dict(row) for row in result]})
    #         for i in range(len(result['result'])):
    #             result["result"][i]['start_date'] = str(result["result"][i]['start_date'])
    #             result["result"][i]['start_time'] = str(result["result"][i]['start_time'])[:-3]
    #             result["result"][i]['end_date'] = str(result["result"][i]['end_date'])
    #             result["result"][i]['end_time'] = str(result["result"][i]['end_time'])[:-3]
    #         return result["result"]
    #     except IntegrityError as e:
    #         return (400, "could not find event")

    # def delete_event_name(self, event_name):
    #     if self.check_event_exists(event_name, "event_name"):
    #         try:
    #             query = self.events.update().values(deleted=True).where(self.events.c.event_name == event_name)
    #             result = self.engine.execute(query)
    #             if result:
    #                 return (True)
    #         except IntegrityError as e:
    #             return (400, "Error updating delete column for " + event_name)
    #     else:
    #         return ("Error finding event " + event_name + " in events table")

    # def delete_event_id(self, event_id):
    #     if self.check_event_exists(event_id, "id"):
    #         try:
    #             query = self.events.update().values(deleted=True).where(self.events.c.id == event_id)
    #             result = self.engine.execute(query)
    #             if result:
    #                 return (True)
    #         except IntegrityError as e:
    #             return ("Error updating delete column for " + event_id)
    #     else:
    #         return ("Error finding event " + str(event_id) + " in events table")
            
    # def create_event(self, token, event_details):
    #     # This function takes a token and a nested dictionary of event details, it flattens 
    #     # the dict, finds a new ID for the new event, gets the host ID and username from the
    #     # token, formats all of the data required for the insertion into the event table and 
    #     # finally returns the event details and event ID

    #     event_details = self.flatten_details(event_details)
    #     new_id = self.get_new_event_id()

    #     host = self.get_host_id_from_token(token)
    #     host_username = self.get_host_username_from_token(token)

    #     insert_data = {}
    #     insert_data['id'] = new_id
    #     insert_data['event_name'] = event_details['title']
    #     insert_data['type'] = event_details['type']
    #     insert_data['location'] = event_details['location']
    #     insert_data['host'] = host
    #     insert_data['host_username'] = host_username
    #     insert_data['deleted'] = False 
    #     insert_data['description'] = event_details['desc']
    #     insert_data['adult_only'] = event_details['cond_adult']
    #     insert_data['vax_only'] = event_details['cond_vax'] 
    #     insert_data['start_date'] = datetime.datetime.strptime(event_details['startdate'], "%Y-%m-%d").date()
    #     insert_data['start_time'] = datetime.datetime.strptime( event_details['starttime'], "%H:%M").time()
    #     insert_data['end_date'] = datetime.datetime.strptime(event_details['enddate'], "%Y-%m-%d").date()
    #     insert_data['end_time'] = datetime.datetime.strptime( event_details['endtime'], "%H:%M").time()
    #     insert_data['gold_num'] = event_details['gold_num']
    #     insert_data['gold_price'] = event_details['gold_price']
    #     insert_data['silver_num'] = event_details['silver_num']
    #     insert_data['silver_price'] = event_details['silver_price']
    #     insert_data['bronze_num'] = event_details['bronze_num']
    #     insert_data['bronze_price'] = event_details['bronze_price']

    #     result = self.insert_events(insert_data), insert_data
    #     return result

    # def update_event(self, event_id, event_details, token):
    #     # TODO:
    #     # 1. Flatten event_details
    #     # 2. Format event_details
    #     # 3. Update row

    #     event_details = self.flatten_details(event_details)
    #     host = self.get_host_id_from_token(token)
    #     host_username = self.get_host_username_from_token(token)

    #     update_data = {}
    #     update_data['event_name'] = event_details['title']
    #     update_data['type'] = event_details['type']
    #     update_data['location'] = event_details['location']
    #     update_data['host'] = host
    #     update_data['host_username'] = host_username
    #     update_data['deleted'] = False 
    #     update_data['description'] = event_details['desc']
    #     update_data['adult_only'] = event_details['cond_adult']
    #     update_data['vax_only'] = event_details['cond_vax'] 
    #     update_data['start_date'] = datetime.datetime.strptime(event_details['startdate'], "%Y-%m-%d").date()
    #     update_data['start_time'] = datetime.datetime.strptime( event_details['starttime'], "%H:%M").time()
    #     update_data['end_date'] = datetime.datetime.strptime(event_details['enddate'], "%Y-%m-%d").date()
    #     update_data['end_time'] = datetime.datetime.strptime( event_details['endtime'], "%H:%M").time()
    #     update_data['gold_num'] = event_details['gold_num']
    #     update_data['gold_price'] = event_details['gold_price']
    #     update_data['silver_num'] = event_details['silver_num']
    #     update_data['silver_price'] = event_details['silver_price']
    #     update_data['bronze_num'] = event_details['bronze_num']
    #     update_data['bronze_price'] = event_details['bronze_price']

    #     try:
    #         update_query = self.events.update().values(update_data).where(self.events.c.id == event_id)
    #         result = self.engine.execute(update_query)
    #         return True
    #     except:
    #         return False

    # def select_all_events(self):
    #     # This funtion currently returns a list of all the rows of the events table
    #     query = db.select([self.events])
    #     try:
    #         result = self.engine.execute(query)
    #         result = ({'result': [dict(row) for row in result]})
    #         for i in range(len(result['result'])):
    #             result["result"][i]['start_date'] = str(result["result"][i]['start_date'])
    #             result["result"][i]['start_time'] = str(result["result"][i]['start_time'])
    #             result["result"][i]['end_date'] = str(result["result"][i]['end_date'])
    #             result["result"][i]['end_time'] = str(result["result"][i]['end_time'])
    #         return result["result"]
    #     except IntegrityError as e:
    #         return (400, "Could not select from table")
    
    # def select_events_hostid(self, host_id):
    #     # This functions searches for events with event_name as event_name and returns a list of all events
    #     query = db.select([self.events]).where(
    #         and_(
    #             self.events.c.host == host_id,
    #             self.events.c.deleted == False
    #             )
    #         )
    #     try:
    #         result = self.engine.execute(query)
    #         result = ({'result': [dict(row) for row in result]})
    #         for i in range(len(result['result'])):
    #             result["result"][i]['start_date'] = str(result["result"][i]['start_date'])
    #             result["result"][i]['start_time'] = str(result["result"][i]['start_time'])
    #             result["result"][i]['end_date'] = str(result["result"][i]['end_date'])
    #             result["result"][i]['end_time'] = str(result["result"][i]['end_time'])
                
    #         return result["result"]
    #     except IntegrityError as e:
    #         return (400, "could not find event")
    
    # def select_events_bytype(self, type):
    #     query = db.select([self.events]).where(
    #         and_(
    #             self.events.c.type == type,
    #             self.events.c.deleted == False
    #             )
    #         )
    #     try:
    #         result = self.engine.execute(query)
    #         result = ({'result': [dict(row) for row in result]})
    #         for i in range(len(result['result'])):
    #             result["result"][i]['start_date'] = str(result["result"][i]['start_date'])
    #             result["result"][i]['start_time'] = str(result["result"][i]['start_time'])
    #             result["result"][i]['end_date'] = str(result["result"][i]['end_date'])
    #             result["result"][i]['end_time'] = str(result["result"][i]['end_time'])
                
    #         return result["result"]
    #     except IntegrityError as e:
    #         return (400, "could not find event")

    # def check_event_exists(self, event_detail, event_col):
    #     event_exists = False

    #     if event_col == "id":
    #         check_query = db.select([self.events]).where(self.events.c.id == event_detail)
    #     else: 
    #         check_query = db.select([self.events]).where(self.events.c.event_name == event_detail)
        
    #     check_result = self.engine.execute(check_query).fetchall()
    #     if len(check_result) > 0:
    #         event_exists = True
    #     return event_exists

    # def check_user_exists(self, username):
    #     user_exists = False
    #     check_query = db.select([self.users]).where(self.users.c.username == username)
    #     check_result = self.engine.execute(check_query).fetchall()
    #     if len(check_result) > 0:
    #         user_exists = True
    #     return user_exists

    # def check_passwords_match(self, username, password):
    #     passwords_match = False
    #     check_query = db.select([self.users]).where(
    #         and_(
    #             self.users.c.username == username,
    #             self.users.c.password == password
    #             )
    #         )
    #     check_result = self.engine.execute(check_query).fetchall()
    #     if len(check_result) > 0:
    #             passwords_match = True
    #     return passwords_match
    
    # def get_new_user_id(self):
    #     # returns the highest id in the user table plus 1
    #     query_max_id = db.select([db.func.max(self.users.columns.id)])
    #     max_id = self.engine.execute(query_max_id).scalar()
    #     return max_id + 1

    # def register_new_user(self, username, password):
    #     # need to get new userID
    #     # function to get highest ID value

    #     data = {
    #         "id":self.get_new_user_id(), 
    #         "username": username,
    #         "password": password,
    #         "token": username,
    #         "dateOfBirth": "",
    #         "vaccinated": ""
    #     }

    #     try:
    #         new_id = self.insert_users(data, False)    
    #         return new_id
    #     except:
    #         return -1
    
    # def check_userid_exists(self, userid):
    #     user_exists = False
    #     check_query = db.select([self.users]).where(self.users.c.id == userid)
    #     check_result = self.engine.execute(check_query).fetchall()
    #     if len(check_result) > 0:
    #         user_exists = True
    #     return user_exists
    
    # def get_user_record(self, userid):
    #     user_query = db.select([self.users]).where(self.users.c.id == userid)
    #     user_result = self.engine.execute(user_query).fetchall()
    #     if len(user_result) > 0:
    #         return user_result
    #     else:
    #         return -1
    
    # def get_user_record_byname(self, username):
    #     user_query = db.select([self.users]).where(self.users.c.username == username)
    #     user_result = self.engine.execute(user_query).fetchall()
    #     if len(user_result) > 0:
    #         return user_result
    #     else:
    #         return -1
    
    # def check_usertoken_exists(self, usertoken):
    #     user_exists = False
    #     check_query = db.select([self.users]).where(self.users.c.token == usertoken)
    #     check_result = self.engine.execute(check_query).fetchall()
    #     if len(check_result) > 0:
    #         user_exists = True
    #     return user_exists
    
    # def update_user_details(self, params, token):
    #     # update_query = self.users.update(). \
    #     # values({
    #     #     'phone': bindparam('phone'),
    #     #     'firstname': bindparam('firstname'),
    #     #     'lastname': bindparam('lastname')
    #     # }).where(self.users.c.token == token)
    #     update_query = self.users.update().values(params).where(self.users.c.token == token)
    #     a = self.engine.execute(update_query)
        
    #     try:
    #         return self.engine.execute(update_query)
    #     except:
    #         return -1

    # def get_new_event_id(self):
    #     # returns the highest id in the user table plus 1
    #     query_max_id = db.select([db.func.max(self.events.columns.id)])
    #     max_id = self.engine.execute(query_max_id).scalar()
    #     return max_id + 1

    # def flatten_details(self, data):
    #     return pd.json_normalize(data, sep='_').to_dict(orient='records')[0]

    # def get_host_id_from_token(self, token):
    #     check_query = db.select([self.users]).where(self.users.c.token == token)
    #     check_result = self.engine.execute(check_query)
    #     check_result = ({'result': [dict(row) for row in check_result]})
    #     list_result = check_result['result']
    #     if len(list_result) > 1:
    #         return "Error - more than one user with this token"
    #     else:
    #         return list_result[0]['id']

    # def get_host_username_from_token(self, token):
    #     check_query = db.select([self.users]).where(self.users.c.token == token)
    #     check_result = self.engine.execute(check_query)
    #     check_result = ({'result': [dict(row) for row in check_result]})
    #     list_result = check_result['result']
    #     if len(list_result) > 1:
    #         return "Error - more than one user with this token"
    #     else:
    #         return list_result[0]['username']
    
    # def select_tickets_event_id(self, event_id):
    #     tickets_query = db.select([self.tickets]).where(
    #         and_(
    #             self.tickets.c.event_id == event_id,
    #             self.tickets.c.purchased == False
    #             )
    #         )
    #     result = self.engine.execute(tickets_query)
    #     result = ({'result': [dict(row) for row in result]})
    #     return result

    # def reserve_tickets(self, data, user_id):
    #     data = json.loads(data.replace("'", '"'))
    #     card_number = data['card_number']
    #     update_query = self.tickets.update().values(purchased=True, user_id=user_id, card_number=card_number).where(
    #         and_(
    #             self.tickets.c.event_id == data['event_id'],
    #             self.tickets.c.seat_num == data['seat_num'],
    #             self.tickets.c.tix_class == data['tix_class']
    #             )
    #         )
    #     result = self.engine.execute(update_query)
    #     return result

    # def refund_tickets(self, data, user_id):
    #     data = json.loads(data.replace("'", '"'))
    #     update_query = self.tickets.update().values(purchased=db.false(), user_id=db.null(), card_number=db.null()).where(
    #         and_(
    #             self.tickets.c.user_id == user_id,
    #             self.tickets.c.event_id == data['event_id'],
    #             self.tickets.c.seat_num == data['seat_num'],
    #             self.tickets.c.tix_class == data['tix_class']
    #             )
    #         )
    #     result = self.engine.execute(update_query)
    #     return result

    # def select_all_tickets(self, user_id):
    #     user_tickets_query = db.select([self.tickets]).where(
    #         and_(
    #             self.tickets.c.user_id == user_id,
    #             self.tickets.c.purchased == True
    #             )
    #         )
    #     result = self.engine.execute(user_tickets_query)
    #     result = ({'result': [dict(row) for row in result]})
    #     return result

    # def get_event_time_date(self, event_id):
    #     event_start_query = db.select([self.events]).where(self.events.c.id == event_id)
    #     result = self.engine.execute(event_start_query)
    #     result = ({'result': [dict(row) for row in result]})
    #     start_date = str(result['result'][0]['start_date'])
    #     start_time = str(result['result'][0]['start_time'])
    #     event_name = result['result'][0]['event_name']
    #     return start_date, start_time, event_name