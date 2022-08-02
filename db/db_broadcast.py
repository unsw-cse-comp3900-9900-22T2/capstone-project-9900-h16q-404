

# import third party libaries
from sqlalchemy.exc import IntegrityError
import sqlalchemy as db
from sqlalchemy import and_
import datetime


class BroadcastDB:
    def __init__(self):
        from app import databaseTables

        self.temp_db = databaseTables

    def get_new_broadcast_id(self):
        # returns the highest id in the user table plus 1
        query_max_id = db.select([db.func.max(self.temp_db.broadcast.columns.id)])
        max_id = self.temp_db.engine.execute(query_max_id).scalar()
        if max_id == None:
            max_id = 0
        return max_id + 1
    
    def post_broadcast(self, eventId, msg):
        
        data = {
            "id":self.get_new_broadcast_id(), 
            "eventId": eventId,
            "message": msg
        }

        try:
            new_id = self.insert_broadcast(data)
            return new_id
        except:
            return -1
    
    def get_alluser_record(self):
        user_query = db.select([self.temp_db.users])
        user_result = self.temp_db.engine.execute(user_query).fetchall()
        if len(user_result) > 0:
            return user_result
        else:
            return -1
    
    def get_userid_with_tickets(self, eventId):
        user_ticket_query = db.select([self.temp_db.tickets]).where(self.temp_db.tickets.c.event_id == eventId)
        userid_with_tickets = set()
        
        try:
            result = self.temp_db.engine.execute(user_ticket_query)
            result = ({'result': [dict(row) for row in result if row["user_id"] != None]})
            
            for i in range(len(result['result'])):
                
                userid_with_tickets.add(result["result"][i]['user_id'])
            
            return userid_with_tickets
        except IntegrityError as e:
            return (400, "could not find review for event")


    def insert_broadcast(self, data):
        insert_check = True
        check_query = db.select([self.temp_db.broadcast]).where(self.temp_db.broadcast.c.id == data["id"])
        check_result = self.temp_db.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})
        for i in range(len(check_result['result'])):
             if data["id"] == (check_result["result"][i]['id']):
                insert_check = False
        
        # if no row exists with current primary key add new row
        if insert_check == True:
            query = db.insert(self.temp_db.broadcast).values(
                id = data["id"],
                eventId = data["eventId"],
                message = data["message"]
            )
            try:
                result = self.temp_db.engine.execute(query).inserted_primary_key 
                return result 
            except:
                return -1
        else:
            print("Broadcast Message " + str(data["id"]) + " not added to broadcast table as it failed the insert check")