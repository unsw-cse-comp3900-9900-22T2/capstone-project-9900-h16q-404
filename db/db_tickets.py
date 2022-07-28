
from db.init_db import InitDB
import sqlalchemy as db
from sqlalchemy import and_
import json

class TicketsDB:
    def __init__(self):
        self.temp_db = InitDB()

    def select_tickets_event_id(self, event_id):
        tickets_query = db.select([self.temp_db.tickets]).where(
            and_(
                self.temp_db.tickets.c.event_id == event_id,
                self.temp_db.tickets.c.purchased == False
                )
            )
        result = self.temp_db.engine.execute(tickets_query)
        result = ({'result': [dict(row) for row in result]})
        return result

    def reserve_tickets(self, data, user_id):
        data = json.loads(data.replace("'", '"'))
        card_number = data['card_number']
        update_query = self.temp_db.tickets.update().values(purchased=True, user_id=user_id, card_number=card_number).where(
            and_(
                self.temp_db.tickets.c.event_id == data['event_id'],
                self.temp_db.tickets.c.seat_num == data['seat_num'],
                self.temp_db.tickets.c.tix_class == data['tix_class']
                )
            )
        result = self.temp_db.engine.execute(update_query)
        return result

    def refund_tickets(self, data, user_id):
        data = json.loads(data.replace("'", '"'))
        update_query = self.temp_db.tickets.update().values(purchased=db.false(), user_id=db.null(), card_number=db.null()).where(
            and_(
                self.temp_db.tickets.c.user_id == user_id,
                self.temp_db.tickets.c.event_id == data['event_id'],
                self.temp_db.tickets.c.seat_num == data['seat_num'],
                self.temp_db.tickets.c.tix_class == data['tix_class']
                )
            )
        result = self.temp_db.engine.execute(update_query)
        return result

    def pre_fill_tickets(self, data):
        self.insert_tix(data['gold_num'], 'gold', data['id'], data['gold_price'])
        self.insert_tix(data['silver_num'], 'silver', data['id'], data['silver_price'])
        self.insert_tix(data['bronze_num'], 'bronze', data['id'], data['bronze_price'])

    def insert_tix(self, num_tix, tix_class, event_ID, price):
        for i in range(num_tix):
            query = db.insert(self.temp_db.tickets).values(
                id = self.temp_db.get_max_ticket_id(),
                event_id = event_ID,
                tix_class = tix_class,
                seat_num = i,
                purchased = False,
                ticket_price = price
            )
            result = self.temp_db.engine.execute(query).inserted_primary_key

    def get_max_ticket_id(self):
        # returns the highest id in the tickets table plus 1
        query_max_id = db.select([db.func.max(self.temp_db.tickets.columns.id)])
        max_id = self.temp_db.engine.execute(query_max_id).scalar()
        if max_id == None:
            max_id = 0
        return max_id + 1