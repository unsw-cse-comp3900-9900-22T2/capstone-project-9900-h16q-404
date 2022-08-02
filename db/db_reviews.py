
# import third party libaries
from sqlalchemy.exc import IntegrityError
import sqlalchemy as db
from sqlalchemy import and_
import datetime


class ReviewsDB:
    def __init__(self):
        from app import databaseTables

        self.temp_db = databaseTables

    def get_event_hostname(self, event_id):
        # This functions returns the host name of the event with wvent_id
        query_host = db.select([self.temp_db.events]).where(self.temp_db.events.c.id == event_id)
        try:
            result = self.temp_db.engine.execute(query_host)
            result = ({'result': [dict(row) for row in result]})
            return result["result"][0]['host_username']
        except IntegrityError as e:
            return (400, "could not find event")


    def check_user_isHost(self, userId, eventId):
        event_host_query = db.select([self.temp_db.events]).where(self.temp_db.events.c.id == eventId)
        try:
            result = self.temp_db.engine.execute(event_host_query)
            result = ({'result': [dict(row) for row in result]})
            event_host = result["result"][0]['host']
            
            return event_host == userId
        except IntegrityError as e:
            return (400, "could not find review for event")
    
    def check_user_hasTicket(self, userId, eventId):
        user_ticket_query = db.select([self.temp_db.tickets]).where(
            and_(
                self.temp_db.tickets.c.user_id == userId,
                self.temp_db.tickets.c.event_id == eventId
                )
            )
        result = self.temp_db.engine.execute(user_ticket_query)
        result = ({'result': [dict(row) for row in result]})
        if (len(result['result']) > 0):
            return True
        else:
            return False
    
    def check_user_hasComment(self, userId, eventId):
        user_comment_query = db.select([self.temp_db.reviews]).where(
            and_(
                self.temp_db.reviews.c.userId == userId,
                self.temp_db.reviews.c.eventId == eventId
                )
            )
        result = self.temp_db.engine.execute(user_comment_query)
        result = ({'result': [dict(row) for row in result]})
        if (len(result['result']) > 0):
            return True
        else:
            return False

    def get_reviews_by_eventId(self, eventId):
        event_review_query = db.select([self.temp_db.reviews]).where(self.temp_db.reviews.c.eventId == eventId)
        try:
            result = self.temp_db.engine.execute(event_review_query)
            result = ({'result': [dict(row) for row in result]})
            for i in range(len(result['result'])):
                result["result"][i]['reviewTimeStamp'] = str(result["result"][i]['reviewTimeStamp'])
                result["result"][i]['replyTimeStamp'] = str(result["result"][i]['replyTimeStamp'])
                
            return result["result"]
        except IntegrityError as e:
            return (400, "could not find review for event")

    def get_username_from_id(self, id):
        check_query = db.select([self.temp_db.users]).where(self.temp_db.users.c.id == id)
        check_result = self.temp_db.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})
        list_result = check_result['result']
        if len(list_result) > 1:
            return "Error - more than one user with this token"
        else:
            return list_result[0]['username']


    def check_eventid_exists(self, eventId):
        event_exists = False
        check_query = db.select([self.temp_db.events]).where(self.temp_db.events.c.id == eventId)
        check_result = self.temp_db.engine.execute(check_query).fetchall()
        if len(check_result) > 0:
            event_exists = True
        return event_exists

    def post_review(self, userId, eventId, timeStamp, comment, rating, host, eventType):
        
        data = {
            "id":self.get_new_review_id(), 
            "eventId": eventId,
            "userId": userId,
            "reviewTimeStamp": datetime.datetime.strptime(timeStamp, "%Y-%m-%d %H:%M"),
            "review": comment,
            "rating": rating,
            "host": host,
            "eventType": eventType
        }

        try:
            new_id = self.insert_reviews(data, False)
            return new_id
        except:
            return -1

    def update_user_reviews(self, params, userId, eventId):
        
        update_query = self.temp_db.reviews.update().values(params).where(
            and_(
                self.temp_db.reviews.c.userId == userId,
                self.temp_db.reviews.c.eventId == eventId
                )
            )
        
        try:
            return self.temp_db.engine.execute(update_query)
        except:
            return -1

    def delete_user_reviews(self, userId, eventId):
        delete_query = self.temp_db.reviews.delete().where(
            and_(
                self.temp_db.reviews.c.userId == userId,
                self.temp_db.reviews.c.eventId == eventId
                )
            )
        
        try:
            return self.temp_db.engine.execute(delete_query)
        except:
            return -1

    def get_new_review_id(self):
        # returns the highest id in the user table plus 1
        query_max_id = db.select([db.func.max(self.temp_db.reviews.columns.id)])
        max_id = self.temp_db.engine.execute(query_max_id).scalar()
        if max_id is None:
            return 1
        return max_id + 1

    def insert_reviews(self, data, dummy):
        insert_check = True
        check_query = db.select([self.temp_db.reviews]).where(self.temp_db.reviews.c.id == data["id"])
        check_result = self.temp_db.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})
        for i in range(len(check_result['result'])):
             if data["id"] == (check_result["result"][i]['id']):
                insert_check = False
        
        # if no row exists with current primary key add new row
        if insert_check == True:
            if dummy == True:
                query = db.insert(self.temp_db.reviews).values(
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
                query = db.insert(self.temp_db.reviews).values(
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
                result = self.temp_db.engine.execute(query).inserted_primary_key 
                return result 
            except:
                return -1
        else:
            print("Review " + str(data["id"]) + " not added to reviews table as it failed the insert check")

    def select_event_byId(self, eventId):
        # This functions searches for events with event_name as event_name and returns a list of all events
        query = db.select([self.temp_db.events]).where(
            and_(
                self.temp_db.events.c.id == eventId,
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

    def update_user_reviews(self, params, userId, eventId):
        
        update_query = self.temp_db.reviews.update().values(params).where(
            and_(
                self.temp_db.reviews.c.userId == userId,
                self.temp_db.reviews.c.eventId == eventId
                )
            )
        
        try:
            return self.temp_db.engine.execute(update_query)
        except:
            return -1