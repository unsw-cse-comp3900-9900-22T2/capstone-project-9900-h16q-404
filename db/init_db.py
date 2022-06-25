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
from psycopg2 import IntegrityError
import sqlalchemy as db
from sqlalchemy import select
import pandas as pd
from datetime import datetime
from flask import jsonify

# InitDB class
class InitDB:
    # This function is run upon creating an instance of the class
    def __init__(self):
        # create engine and connect to databse in the db folder
        self.engine = db.create_engine('sqlite:///db\group_404')
        # Metadata is a container object that kees together many of the different features fo a db
        self.metadata = db.MetaData()
        
        # Define the events tables
        self.events = db.Table('events', self.metadata,
            db.Column('id', db.Integer(), primary_key=True),
            db.Column('event_name', db.String(255), nullable=False),
            db.Column('event_date', db.Date, nullable=False)
        )
        
        # create all objects in the metadata object
        self.metadata.create_all(self.engine, checkfirst=True)

    def fill_with_dummy_data(self):
        # This function will read one or more CSVs and then insert the data from those CSVs into the relevant tables
        dummy_events_df = pd.read_csv("db\dummy_events.csv")

        # Iterate through pandas DF and insert each row into table using insert function
        for index, row in dummy_events_df.iterrows():
            data = {
                "id":row.id, 
                "event_name": row.event_name,
                "event_date": datetime.fromisoformat(row.event_date)
            }
            self.insert_events(data)

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
                event_date = data["event_date"]
            )
            try:
                ResultProxy = self.engine.execute(query).inserted_primary_key
                print(ResultProxy)
            except IntegrityError as e:
                return (400, "Could not insert into table")
        else:
            print("Item not added as it failed the insert check")

    def select_all_events(self):
        # This funtion currently returns a list of all the rows of the events table
        query = db.select([self.events])
        try:
            result = self.engine.execute(query)
            result = ({'result': [dict(row) for row in result]})
            for i in range(len(result['result'])):
                result["result"][i]['event_date'] = str(result["result"][i]['event_date'])
            print(result)
            return result["result"]
        except IntegrityError as e:
            return (400, "Could not select from table")

    def check_user_exists(self, username):
        # select all users with username
        # if username exists return True
        # else return false
        return True
    
    
# The main function creates an InitDB class and then calls the fill_with_dummy_data method
def db_main():
    db = InitDB()
    db.fill_with_dummy_data()