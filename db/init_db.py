from psycopg2 import IntegrityError
import sqlalchemy as db
from sqlalchemy import select
import pandas as pd
from datetime import datetime
from flask import jsonify

class InitDB:
    def __init__(self):
        self.engine = db.create_engine('sqlite:///db\group_404')
        self.metadata = db.MetaData()
        self.events = db.Table('events', self.metadata,
            db.Column('id', db.Integer(), primary_key=True),
            db.Column('event_name', db.String(255), nullable=False),
            db.Column('event_date', db.Date, nullable=False)
        )
        self.metadata.create_all(self.engine)

    def fill_with_dummy_data(self):
        dummy_events_df = pd.read_csv("db\dummy_events.csv")

        for index, row in dummy_events_df.iterrows():
            print(row.id)
            print(row.event_date)
            data = {
                "id":row.id, 
                "event_name": row.event_name,
                "event_date": datetime.fromisoformat(row.event_date)
            }
            self.insert_events(data)

    def insert_events(self, data):
        print(data)
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

    def select_events(self, id):
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

def db_main():
    db = InitDB()
    db.fill_with_dummy_data()