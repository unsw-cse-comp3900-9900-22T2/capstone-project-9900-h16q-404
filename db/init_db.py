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
<<<<<<< HEAD
from sqlalchemy.exc import IntegrityError
=======
from psycopg2 import IntegrityError
from requests import delete
>>>>>>> origin/VY9900-37_backend_create_event
import sqlalchemy as db
from sqlalchemy import select, and_, func
import pandas as pd
import datetime
from flask import jsonify

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
            db.Column('description', db.String(255), nullable=True)
        )

        # define the users tables
        self.users = db.Table('users', self.metadata,
            db.Column('id', db.Integer(), primary_key=True),
            db.Column('username', db.String(255), nullable=False),
            db.Column('password', db.String(255), nullable=False),
            db.Column('token', db.String(255), nullable=False),
            db.Column('email', db.String(255), nullable=False),
            db.Column('firstName', db.String(255), nullable=True),
            db.Column('lastName', db.String(255), nullable=True),
            db.Column('dateOfBirth', db.Date, nullable=True),
            db.Column('gender', db.String(255), nullable=True),
            db.Column('phone', db.String(255), nullable=True),
            db.Column('vaccinated', db.Boolean(), nullable=True)
        )
        
        # create all objects in the metadata object
        self.metadata.create_all(self.engine, checkfirst=True)

    def fill_dummy_data(self):
        # This function will read one or more CSVs and then insert the data from those CSVs into the relevant tables
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
                "description": row.description
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
                "dateOfBirth" : '',
                "gender" : '',
                "phone" : '',
                "vaccinated" : ''
            }
            #print(data)
            new_id = self.insert_users(data)
            print(new_id)

    def insert_users(self, data):
        insert_check = True
        check_query = db.select([self.users]).where(self.users.c.id == data["id"])
        check_result = self.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})
        print(check_result)
        for i in range(len(check_result['result'])):
             if data["id"] == (check_result["result"][i]['id']):
                insert_check = False
        
        # if no row exists with current primary key add new row
        if insert_check == True:
            query = db.insert(self.users).values(
                id = data["id"],
                username = data["username"],
                password = data["password"],
                token = data["token"],
                email = data['username']
                #firstName = '',
                #lastName = '',
                #dateOfBirth = '',
                #gender = '',
                #phone = '',
                #vaccinated = ''
            )
            try:
                return self.engine.execute(query).inserted_primary_key 
            except:
                return -1
        else:
            print("Item " + str(data["username"]) + " not added to user table as it failed the insert check")


    def insert_events(self, data):
        # This function takes a JSON object "data" and inserts the object into the DB as a new row
        # But first the function checks if a row with the same ID aleady exists
        
        # check for row with existing primary key
        insert_check = True
        check_query = db.select([self.events]).where(self.events.c.id == data["id"])
        check_result = self.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})
        for i in range(len(check_result['result'])):
             if data["id"] == (check_result["result"][i]['id']):
                insert_check = False

        # if no row exists with current primary key add new row
        if insert_check == True:
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
                description = data["description"]
            )
            try:
                return self.engine.execute(query).inserted_primary_key 
            except:
                return -1
        else:
            print("Item " + str(data["event_name"]) + " not added to events table as it failed the insert check")

    def select_event_name(self, event_name):
        # This functions searches for events with event_name as event_name and returns a list of all events
        query = db.select([self.events]).where(self.events.c.event_name == event_name)
        try:
            result = self.engine.execute(query)
            result = ({'result': [dict(row) for row in result]})
            for i in range(len(result['result'])):
                result["result"][i]['event_date'] = str(result["result"][i]['event_date'])
            return result["result"]
        except IntegrityError as e:
            return (400, "could not find event")

    def select_event_id(self, event_id):
        # This functions searches for events with id as event_id and returns a list of all events
        query = db.select([self.events]).where(self.events.c.id == event_id)
        try:
            result = self.engine.execute(query)
            result = ({'result': [dict(row) for row in result]})
            for i in range(len(result['result'])):
                result["result"][i]['start_date'] = str(result["result"][i]['start_date'])
                result["result"][i]['start_time'] = str(result["result"][i]['start_time'])[:-3]
                result["result"][i]['end_date'] = str(result["result"][i]['end_date'])
                result["result"][i]['end_time'] = str(result["result"][i]['end_time'])[:-3]
            return result["result"]
        except IntegrityError as e:
            return (400, "could not find event")

    def delete_event_name(self, event_name):
        if self.check_event_exists(event_name, "event_name"):
            try:
                query = self.events.update().values(deleted=True).where(self.events.c.event_name == event_name)
                result = self.engine.execute(query)
                if result:
                    return (True)
            except IntegrityError as e:
                return (400, "Error updating delete column for " + event_name)
        else:
            return ("Error finding event " + event_name + " in events table")

    def delete_event_id(self, event_id):
        if self.check_event_exists(event_id, "id"):
            try:
                query = self.events.update().values(deleted=True).where(self.events.c.id == event_id)
                result = self.engine.execute(query)
                if result:
                    return (True)
            except IntegrityError as e:
                return ("Error updating delete column for " + event_id)
        else:
            return ("Error finding event " + str(event_id) + " in events table")
            
    def create_event(self, token, event_details):
        # TODO:
        # 1. Flatten event details - DONE
        # 2. Get new Event ID - DONE
        # 3. Ensure all variables have the right formatting - DONE
        # 4. Get the host ID from the user table - DONE
        # 5. Insert Event details into table - DONE
        # 6. Return Success or Error and new event 

        event_details = self.flatten_details(event_details)
        new_id = self.get_new_event_id()

        host = self.get_host_id_from_token(token)
        host_username = self.get_host_username_from_token(token)

        insert_data = {}
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
        insert_data['id'] = new_id

        return self.insert_events(insert_data), insert_data

    def select_all_events(self):
        # This funtion currently returns a list of all the rows of the events table
        query = db.select([self.events])
        try:
            result = self.engine.execute(query)
            result = ({'result': [dict(row) for row in result]})
            for i in range(len(result['result'])):
                result["result"][i]['start_date'] = str(result["result"][i]['start_date'])
                result["result"][i]['start_time'] = str(result["result"][i]['start_time'])
                result["result"][i]['end_date'] = str(result["result"][i]['end_date'])
                result["result"][i]['end_time'] = str(result["result"][i]['end_time'])
            return result["result"]
        except IntegrityError as e:
            return (400, "Could not select from table")

    def check_event_exists(self, event_detail, event_col):
        event_exists = False

        if event_col == "id":
            check_query = db.select([self.events]).where(self.events.c.id == event_detail)
        else: 
            check_query = db.select([self.events]).where(self.events.c.event_name == event_detail)
        
        check_result = self.engine.execute(check_query).fetchall()
        if len(check_result) > 0:
            event_exists = True
        return event_exists

    def check_user_exists(self, username):
        user_exists = False
        check_query = db.select([self.users]).where(self.users.c.username == username)
        check_result = self.engine.execute(check_query).fetchall()
        if len(check_result) > 0:
            user_exists = True
        return user_exists

    def check_passwords_match(self, username, password):
        passwords_match = False
        check_query = db.select([self.users]).where(
            and_(
                self.users.c.username == username,
                self.users.c.password == password
                )
            )
        check_result = self.engine.execute(check_query).fetchall()
        if len(check_result) > 0:
                passwords_match = True
        return passwords_match
    
    def get_new_user_id(self):
        # returns the highest id in the user table plus 1
        query_max_id = db.select([db.func.max(self.users.columns.id)])
        max_id = self.engine.execute(query_max_id).scalar()
        return max_id + 1

    def register_new_user(self, username, password):
        # need to get new userID
        # function to get highest ID value

        data = {
            "id":self.get_new_user_id(), 
            "username": username,
            "password": password,
            "token": username
        }

        try:
            new_id = self.insert_users(data)        
            return new_id
        except:
            return -1

    
    def check_userid_exists(self, userid):
        user_exists = False
        check_query = db.select([self.users]).where(self.users.c.id == userid)
        check_result = self.engine.execute(check_query).fetchall()
        print(check_result)
        if len(check_result) > 0:
            user_exists = True
        return user_exists
    
    def get_user_record(self, userid):
        user_query = db.select([self.users]).where(self.users.c.id == userid)
        user_result = self.engine.execute(user_query).fetchall()
        #print(user_result)
        if len(user_result) > 0:
            return user_result
        else:
            return -1
    
    def get_user_record_byname(self, username):
        user_query = db.select([self.users]).where(self.users.c.username == username)
        user_result = self.engine.execute(user_query).fetchall()
        #print(user_result)
        if len(user_result) > 0:
            return user_result
        else:
            return -1
    
    def check_usertoken_exists(self, usertoken):
        user_exists = False
        check_query = db.select([self.users]).where(self.users.c.token == usertoken)
        check_result = self.engine.execute(check_query).fetchall()
        print(usertoken)
        print(check_result)
        if len(check_result) > 0:
            user_exists = True
        return user_exists
    
    def update_user_details(self, params, token):
        # update_query = self.users.update(). \
        # values({
        #     'phone': bindparam('phone'),
        #     'firstname': bindparam('firstname'),
        #     'lastname': bindparam('lastname')
        # }).where(self.users.c.token == token)
        update_query = self.users.update().values(params).where(self.users.c.token == token)
        a = self.engine.execute(update_query)
        
        try:
            return self.engine.execute(update_query)
        except:
            return -1
        def get_new_event_id(self):
        # returns the highest id in the user table plus 1
        query_max_id = db.select([db.func.max(self.events.columns.id)])
        max_id = self.engine.execute(query_max_id).scalar()
        return max_id + 1

    def flatten_details(self, data):
        return pd.json_normalize(data, sep='_').to_dict(orient='records')[0]

    def get_host_id_from_token(self, token):
        check_query = db.select([self.users]).where(self.users.c.token == token)
        check_result = self.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})
        list_result = check_result['result']
        if len(list_result) > 1:
            return "Error - more than one user with this token"
        else:
            return list_result[0]['id']

    def get_host_username_from_token(self, token):
        check_query = db.select([self.users]).where(self.users.c.token == token)
        check_result = self.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})
        list_result = check_result['result']
        if len(list_result) > 1:
            return "Error - more than one user with this token"
        else:
            return list_result[0]['username']
    
# The main function creates an InitDB class and then calls the fill_with_dummy_data method
def db_main():
    db = InitDB()
    db.fill_dummy_data()