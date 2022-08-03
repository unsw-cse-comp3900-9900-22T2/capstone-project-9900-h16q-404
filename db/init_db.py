"""
Written by: Group 404
For COMP9900 Project 7 Event Management System

This file defines the InitDB class which currently contains all of the DB initialisation and
querying functions

This file also has a main function, which when called creates an InitDB class and runs the
fill_with_dummy_data function. This function reads dummy data from a csv and inserts it into
the database.
"""

import datetime
import logging
import json

import pandas as pd
from sqlalchemy.exc import IntegrityError
import sqlalchemy as db
from sqlalchemy import ForeignKey, and_

logger = logging.getLogger(__name__)


# InitDB class
class InitDB:
    # This function is run upon creating an instance of the class
    def __init__(self):
        # create engine and connect to databse in the db folder
        self.engine = db.create_engine("sqlite:///db/group_404")
        # Metadata is a container object that kees together many of the
        # different features fo a db
        self.metadata = db.MetaData()

        # Define the events tables
        self.events = db.Table(
            "events",
            self.metadata,
            db.Column("id", db.Integer(), primary_key=True),
            db.Column("event_name", db.String(255), nullable=False),
            db.Column("host", db.Integer(), nullable=True),
            db.Column("host_username", db.String(255), nullable=True),
            db.Column("type", db.String(255), nullable=True),
            db.Column("start_date", db.Date, nullable=True),
            db.Column("start_time", db.Time, nullable=True),
            db.Column("end_date", db.Date, nullable=True),
            db.Column("end_time", db.Time, nullable=True),
            db.Column("deleted", db.Boolean, nullable=True),
            db.Column("location", db.String(255), nullable=True),
            db.Column("adult_only", db.Boolean, nullable=True),
            db.Column("vax_only", db.Boolean, nullable=True),
            db.Column("description", db.String(255), nullable=True),
            db.Column("gold_num", db.Integer(), nullable=True),
            db.Column("gold_price", db.Float(), nullable=True),
            db.Column("silver_num", db.Integer(), nullable=True),
            db.Column("silver_price", db.Float(), nullable=True),
            db.Column("bronze_num", db.Integer(), nullable=True),
            db.Column("bronze_price", db.Float(), nullable=True),
            db.Column("image", db.TEXT(), nullable=True),
        )

        # define the users tables
        self.users = db.Table(
            "users",
            self.metadata,
            db.Column("id", db.Integer(), primary_key=True),
            db.Column("username", db.String(255), nullable=True),
            db.Column("password", db.String(255), nullable=True),
            db.Column("token", db.String(255), nullable=True),
            db.Column("email", db.String(255), nullable=True),
            db.Column("firstName", db.String(255), nullable=True),
            db.Column("lastName", db.String(255), nullable=True),
            db.Column("dateOfBirth", db.Date, nullable=True),
            db.Column("gender", db.String(255), nullable=True),
            db.Column("phone", db.String(255), nullable=True),
            db.Column("vaccinated", db.Boolean(), nullable=True),
            db.Column("image", db.TEXT(), nullable=True),
        )

        # define the tickets table
        self.tickets = db.Table(
            "tickets",
            self.metadata,
            db.Column("id", db.Integer(), primary_key=True),
            db.Column(
                "event_id", db.Integer(), ForeignKey("events.id"), nullable=False
            ),
            db.Column("user_id", db.Integer(), ForeignKey("users.id"), nullable=True),
            db.Column("seat_num", db.Integer(), nullable=False),
            db.Column("tix_class", db.String(10), nullable=False),
            db.Column("purchased", db.Boolean(), nullable=False),
            db.Column("card_number", db.Integer(), nullable=True),
            db.Column("ticket_price", db.String(16), nullable=False),
        )

        # define the watchlist table
        self.watchlist = db.Table(
            "watchlist",
            self.metadata,
            db.Column("id", db.Integer(), primary_key=True),
            db.Column("follower", db.Integer(), ForeignKey("users.id"), nullable=False),
            db.Column(
                "following", db.Integer(), ForeignKey("users.id"), nullable=False
            ),
        )

        # define the reviews table
        self.reviews = db.Table('reviews', self.metadata,
            db.Column('id', db.Integer(), primary_key=True),
            db.Column('eventId', db.Integer(), ForeignKey('events.id'), nullable=False),
            db.Column('userId', db.Integer(), ForeignKey('users.id'), nullable=False),
            db.Column('reviewTimeStamp', db.DateTime(), nullable=False),
            db.Column('review', db.Text(), nullable=False),
            db.Column('rating', db.Integer(), nullable=True),
            db.Column('replyTimeStamp', db.DateTime(), nullable=True),
            db.Column('reply', db.Text(), nullable=True),
            db.Column('host', db.Text(), nullable=True),
            db.Column('eventType', db.Text(), nullable=True)
        )

        # define the broadcast table
        self.broadcast = db.Table('broadcast', self.metadata,
            db.Column('id', db.Integer(), primary_key=True),
            db.Column('eventId', db.Integer(), ForeignKey('events.id'), nullable=False),
            db.Column('message', db.Text(), nullable=False)
        )

        # create all objects in the metadata object
        self.metadata.create_all(self.engine, checkfirst=True)

    def fill_dummy_data(self):
        # This function will read one or more CSVs and then insert the data
        # from those CSVs into the relevant tables

        # read in dummy data from CSVs
        dummy_events_df = pd.read_csv("db/dummy_data/dummy_events.csv", delimiter="|")
        dummy_users_df = pd.read_csv(
            "db/dummy_data/dummy_users.csv", delimiter="|")
        dummy_tickets_df = pd.read_csv(
            "db/dummy_data/dummy_tickets.csv", delimiter="|")
        dummy_reviews_df = pd.read_csv(
            "db/dummy_data/dummy_reviews.csv", delimiter="|")

        # Iterate through events pandas DF and insert each row into table using
        # insert function
        for index, row in dummy_events_df.iterrows():
            data = {
                "id": row.id,
                "event_name": row.event_name,
                "host": row.host,
                "host_username": row.host_username,
                "type": row.type,
                "start_date": datetime.datetime.strptime(
                    row.start_date, "%d-%m-%Y"
                ).date(),
                "start_time": datetime.datetime.strptime(
                    row.start_time, "%H:%M"
                ).time(),
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
                "image": row.image,
            }
            result = self.insert_events(data)
            if result is None or result == -1:
                print(data["event_name"] + " Not Added")
            else:
                print("Added new event with ID = " + str(result))

        for index, row in dummy_users_df.iterrows():
            data = {
                "id": row.id,
                "username": row.username,
                "password": row.password,
                "token": row.token,
                "email": row.username,
                "firstName": "",
                "lastName": "",
                "dateOfBirth": datetime.datetime.strptime(row.dob, "%Y-%m-%d").date(),
                "gender": "",
                "phone": "",
                "vaccinated": row.vac,
                "image": row.image,
            }
            self.insert_users(data, True)

        # insert dummy tickets
        for index, row in dummy_tickets_df.iterrows():
            user_id = row.user_id
            data = {
                "id":row.id, 
                "event_id": row.event_id,
                "user_id": row.user_id,
                "seat_num": row.seat_num,
                "tix_class" : row.tix_class,
                "purchased" : row.purchased,
                "card_number" : row.card_number,
                "ticket_price" : row.ticket_price
            }
            result = self.reserve_tickets(data, user_id)
            if result == None or result == -1:
                print(str(data["id"]) + " Not Added")
            else:
                print("Added new ticket with ID = " + str(result))

        for index, row in dummy_reviews_df.iterrows():
            data = {
                "id":row.id, 
                "eventId": row.eventId,
                "userId": row.userId,
                "reviewTimeStamp": datetime.datetime.strptime(row.reviewTimeStamp, "%Y-%m-%d %H:%M"),
                "review" : row.review,
                "rating" : row.rating,
                "replyTimeStamp" : datetime.datetime.strptime(row.replyTimeStamp, "%Y-%m-%d %H:%M"),
                "reply" : row.reply,
                "host" : row.host,
                "eventType" : row.eventType
            }
            result = self.insert_reviews(data, True)
            if result == None or result == -1:
                print(str(data["id"]) + " Not Added")
            else:
                print("Added new review with ID = " + str(result))

    def insert_users(self, data, dummy):

        # check for row with existing primary key
        insert_bool = self.insert_check_users(data)

        # if no row exists with current primary key add new row
        if insert_bool is True:
            if dummy is True:
                query = db.insert(self.users).values([data])
            try:
                return self.engine.execute(query).inserted_primary_key
            except IntegrityError:
                return -1
        else:
            print(
                "Item "
                + str(data["username"])
                + " not added to user table as it failed the insert check"
            )

    def insert_events(self, data):
        # This function takes a JSON object "data" and inserts the object into the DB as a new row
        # But first the function checks if a row with the same ID aleady exists

        # check for row with existing primary key
        insert_bool = self.insert_check_events(data)

        # if no row exists with current primary key add new row
        if insert_bool is True:
            query = db.insert(self.events).values(
                id=data["id"],
                event_name=data["event_name"],
                host=data["host"],
                host_username=data["host_username"],
                type=data["type"],
                start_date=data["start_date"],
                start_time=data["start_time"],
                end_date=data["end_date"],
                end_time=data["end_time"],
                deleted=data["deleted"],
                location=data["location"],
                adult_only=data["adult_only"],
                vax_only=data["vax_only"],
                description=data["description"],
                gold_num=data["gold_num"],
                gold_price=data["gold_price"],
                silver_num=data["silver_num"],
                silver_price=data["silver_price"],
                bronze_num=data["bronze_num"],
                bronze_price=data["bronze_price"],
                image=data["image"],
            )
            try:
                result = self.engine.execute(query).inserted_primary_key
                self.pre_fill_tickets(data)
                return result
            except IntegrityError:
                return -1
        else:
            print(
                "Item "
                + str(data["event_name"])
                + " not added to events table as it failed the insert check"
            )

    def pre_fill_tickets(self, data):
        self.insert_tix(data["gold_num"], "gold", data["id"], data["gold_price"])
        self.insert_tix(data["silver_num"], "silver", data["id"], data["silver_price"])
        self.insert_tix(data["bronze_num"], "bronze", data["id"], data["bronze_price"])

    def insert_tix(self, num_tix, tix_class, event_ID, price):
        for i in range(num_tix):
            query = db.insert(self.tickets).values(
                id=self.get_max_ticket_id(),
                event_id=event_ID,
                tix_class=tix_class,
                seat_num=i,
                purchased=False,
                ticket_price=price,
            )
            try:
                self.engine.execute(query).inserted_primary_key
            except IntegrityError:
                print("Error inserting ticket for", str(event_ID))


    def reserve_tickets(self, data, user_id):
        card_number = data["card_number"]
        update_query = (
            self.tickets.update()
            .values(purchased=True, user_id=user_id, card_number=card_number)
            .where(
                and_(
                    self.tickets.c.event_id == data["event_id"],
                    self.tickets.c.seat_num == data["seat_num"],
                    self.tickets.c.tix_class == data["tix_class"],
                )
            )
        )
        result = self.engine.execute(update_query)
        return result

    def get_max_ticket_id(self):
        # returns the highest id in the tickets table plus 1
        query_max_id = db.select([db.func.max(self.tickets.columns.id)])
        max_id = self.engine.execute(query_max_id).scalar()
        if max_id is None:
            max_id = 0
        return max_id + 1

    def select_all_tickets(self, user_id):
        user_tickets_query = db.select([self.tickets]).where(
            and_(self.tickets.c.user_id == user_id, self.tickets.c.purchased is True)
        )
        result = self.engine.execute(user_tickets_query)
        result = {"result": [dict(row) for row in result]}
        return result

    def get_event_time_date(self, event_id):
        event_start_query = db.select([self.events]).where(self.events.c.id == event_id)
        result = self.engine.execute(event_start_query)
        result = {"result": [dict(row) for row in result]}
        start_date = str(result["result"][0]["start_date"])
        start_time = str(result["result"][0]["start_time"])
        event_name = result["result"][0]["event_name"]
        return start_date, start_time, event_name

    def get_max_watchlist_id(self):
        # returns the highest id in the tickets table plus 1
        query_max_id = db.select([db.func.max(self.watchlist.columns.id)])
        max_id = self.engine.execute(query_max_id).scalar()
        if max_id is None:
            max_id = 0
        return max_id + 1

    def check_follower(self, follower_id, following_id):

        check_follower_query = db.select([self.watchlist]).where(
            and_(
                self.watchlist.c.follower == follower_id,
                self.watchlist.c.following == following_id,
            )
        )
        result = self.engine.execute(check_follower_query)
        result = {"result": [dict(row) for row in result]}

        if len(result["result"]) > 0:
            return True
        else:
            return False

    def add_follower(self, follower_id, following_id):

        if self.check_follower(follower_id, following_id) is False:
            try:
                query = db.insert(self.watchlist).values(
                    id=self.get_max_watchlist_id(),
                    follower=follower_id,
                    following=following_id,
                )
                self.engine.execute(query).inserted_primary_key
                return "Success: Added to watchlist"
            except DatabaseExecutionError as e:
                logger.exception(e)
                return "ERROR: Could not add to watchlist"
        else:
            return "ERROR: Already a follower"

    def delete_follower(self, follower_id, following_id):

        if self.check_follower(follower_id, following_id) is True:
            try:
                delete_follower_query = db.delete(self.watchlist).where(
                    and_(
                        self.watchlist.c.follower == follower_id,
                        self.watchlist.c.following == following_id,
                    )
                )
                self.engine.execute(delete_follower_query)
                return "Success"
            except DatabaseExecutionError as e:
                logger.exception(e)
                return "ERROR: Could not remove from watchlist"
        else:
            return "ERROR: You do not follow this user"

    def get_all_following_user_ids(self, user_id):

        check_follower_query = db.select([self.watchlist]).where(
            self.watchlist.c.follower == user_id
        )
        result = self.engine.execute(check_follower_query)
        result = {"result": [dict(row) for row in result]}
        return result["result"]

    def insert_check_users(self, data):

        check_query = db.select([self.users]).where(self.users.c.id == data["id"])
        check_result = self.engine.execute(check_query)
        check_result = {"result": [dict(row) for row in check_result]}

        insert_bool = True
        for i in range(len(check_result["result"])):
            if data["id"] == (check_result["result"][i]["id"]):
                insert_bool = False
        return insert_bool

    def insert_check_events(self, data):

        check_query = db.select([self.events]).where(self.events.c.id == data["id"])
        check_result = self.engine.execute(check_query)
        check_result = {"result": [dict(row) for row in check_result]}

        insert_bool = True
        for i in range(len(check_result["result"])):
            if data["id"] == (check_result["result"][i]["id"]):
                insert_bool = False
        return insert_bool

    def insert_reviews(self, data, dummy):
        insert_check = True
        check_query = db.select([self.reviews]).where(self.reviews.c.id == data["id"])
        check_result = self.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})
        for i in range(len(check_result['result'])):
             if data["id"] == (check_result["result"][i]['id']):
                insert_check = False
        
        # if no row exists with current primary key add new row
        if insert_check == True:
            if dummy == True:
                query = db.insert(self.reviews).values(
                    id = data["id"],
                    eventId = data["eventId"],
                    userId = data["userId"],
                    reviewTimeStamp = data["reviewTimeStamp"],
                    review = data['review'],
                    rating = data['rating'],
                    replyTimeStamp = data['replyTimeStamp'],
                    reply = data['reply'],
                    host = data['host'],
                    eventType = data['eventType']
                )
            else:
                query = db.insert(self.reviews).values(
                    id = data["id"],
                    eventId = data["eventId"],
                    userId = data["userId"],
                    reviewTimeStamp = data["reviewTimeStamp"],
                    review = data['review'],
                    rating = data['rating'],
                    host = data['host'],
                    eventType = data['eventType']
                )
            
            try:
                result = self.engine.execute(query).inserted_primary_key 
                return result 
            except:
                return -1
        else:
            print("Review " + str(data["id"]) + " not added to reviews table as it failed the insert check")


class DatabaseExecutionError(Exception):
    """Raised when a query applied to a database fails"""

    pass


# The main function creates an InitDB class and then calls the
# fill_with_dummy_data method
def db_main():
    db = InitDB()
    db.fill_dummy_data()
    return db