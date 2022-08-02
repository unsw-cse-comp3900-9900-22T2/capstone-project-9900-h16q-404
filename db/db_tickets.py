"""
Functions:
# get/select
- select_tickets_event_id
- select_all_tickets
# create/insert
- insert_tix
- reserve_tickets
# update
# delete
- refund_tickets
# helper
- pre_fill_tickets
- get_max_ticket_id
"""

# import third party libaries
import json
import sqlalchemy as db
from sqlalchemy import and_


class TicketsDB:
    def __init__(self):
        from app import databaseTables

        self.temp_db = databaseTables

    # Functions for selecting/getting from the tickets table

    def select_tickets_event_id(self, event_id):
        tickets_query = db.select([self.temp_db.tickets]).where(
            and_(
                self.temp_db.tickets.c.event_id == event_id,
                self.temp_db.tickets.c.purchased == False,
            )
        )
        result = self.temp_db.engine.execute(tickets_query)
        result = {"result": [dict(row) for row in result]}
        return result

    def select_all_tickets(self, user_id):
        user_tickets_query = db.select([self.temp_db.tickets]).where(
            and_(
                self.temp_db.tickets.c.user_id == user_id,
                self.temp_db.tickets.c.purchased == True,
            )
        )
        result = self.temp_db.engine.execute(user_tickets_query)
        result = {"result": [dict(row) for row in result]}
        return result

    # Functions for inserting/reserving tickets

    def insert_tix(self, num_tix, tix_class, event_ID, price):
        for i in range(num_tix):
            query = db.insert(self.temp_db.tickets).values(
                id=self.temp_db.get_max_ticket_id(),
                event_id=event_ID,
                tix_class=tix_class,
                seat_num=i,
                purchased=False,
                ticket_price=price,
            )
            self.temp_db.engine.execute(query).inserted_primary_key

    def reserve_tickets(self, data, user_id):
        data = json.loads(data.replace("'", '"'))
        card_number = data["card_number"]
        update_query = (
            self.temp_db.tickets.update()
            .values(purchased=True, user_id=user_id, card_number=card_number)
            .where(
                and_(
                    self.temp_db.tickets.c.event_id == data["event_id"],
                    self.temp_db.tickets.c.seat_num == data["seat_num"],
                    self.temp_db.tickets.c.tix_class == data["tix_class"],
                )
            )
        )
        result = self.temp_db.engine.execute(update_query)
        return result

    # Functions for deleting/refunding tickets

    def refund_tickets(self, data, user_id):
        data = json.loads(data.replace("'", '"'))
        update_query = (
            self.temp_db.tickets.update()
            .values(purchased=db.false(), user_id=db.null(), card_number=db.null())
            .where(
                and_(
                    self.temp_db.tickets.c.user_id == user_id,
                    self.temp_db.tickets.c.event_id == data["event_id"],
                    self.temp_db.tickets.c.seat_num == data["seat_num"],
                    self.temp_db.tickets.c.tix_class == data["tix_class"],
                )
            )
        )
        result = self.temp_db.engine.execute(update_query)
        return result

    # Helper functions

    def pre_fill_tickets(self, data):
        self.insert_tix(data["gold_num"], "gold", data["id"], data["gold_price"])
        self.insert_tix(data["silver_num"], "silver", data["id"], data["silver_price"])
        self.insert_tix(data["bronze_num"], "bronze", data["id"], data["bronze_price"])

    def get_max_ticket_id(self):
        # returns the highest id in the tickets table plus 1
        query_max_id = db.select([db.func.max(self.temp_db.tickets.columns.id)])
        max_id = self.temp_db.engine.execute(query_max_id).scalar()
        if max_id is None:
            max_id = 0
        return max_id + 1
