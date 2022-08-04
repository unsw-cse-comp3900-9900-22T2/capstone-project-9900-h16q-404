# import custom classes used to interact with the DB
from db.db_broadcast import BroadcastDB
from db.db_events import EventsDB
from api.exceptions import DatabaseExecutionError

# import third party libaries
from flask_restful import Resource, reqparse
from flask import request
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Broadcast(Resource):
    def post(self):
        getRequest = request.json
        if ('eventId' in getRequest):
            eventId = getRequest['eventId']
        else:
            return {"status": "Error", "message": "Event Id was not Sent"}
        
        if ('msg' in getRequest):
            messageToBroadcast = getRequest['msg']
        else:
            return {"status": "Error", "message": "msg was not Sent"}
        
        # create db engine
        broadcast_db = BroadcastDB()
        events_db = EventsDB()
        
        
        # post message to broadcast table
        new_id = broadcast_db.post_broadcast(eventId, messageToBroadcast)
        
        # get email of all users who have tickets to eventId
        get_users = broadcast_db.get_alluser_record()
        users_dict = {}
        
        if (len(get_users) > 0):
            for user in get_users:
                get_name = user['username'].split('@')[0].replace("."," ").title()
                users_dict[user['id']] = (user['username'], get_name)
        
        # fetch all user id from tickets for eventId
        user_has_tickets = broadcast_db.get_userid_with_tickets(eventId)
        user_mail_list = []
        
        if (len(user_has_tickets) > 0):
            for user in user_has_tickets:
                user_mail_list.append(users_dict[user])

        to_emails = user_mail_list
        #to_emails = "g.jayaraman@student.unsw.edu.au"
        sender_email = os.environ.get('MAIL_DEFAULT_SENDER')
        sender_name = os.environ.get('MAIL_SENDER_NAME')
        # Email Subject compose
        get_event = events_db.select_event_id(eventId)
        
        try:
            subject_msg = "Update For " + get_event[0]['event_name'] + " (From Group:404 Platform)"
        except:
            subject_msg = 'Hello'
        
        message = Mail(
        from_email=(sender_email, sender_name),
        subject=subject_msg,
        plain_text_content=messageToBroadcast,
        to_emails=to_emails,
        is_multiple=True)
        
        if (len(to_emails) > 0):
            try:
                sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message)
            except Exception as e:
                return {"status": "Error", "message": "Error broadcasting message to ticket holders"}
            
            return {
                'resultStatus': 'SUCCESS',
                'message': "Successfully broadcasted email to all ticket holders for this event"
            }
        else:
            return {
                'status': 'Error',
                'message': "No email sent as no one has bought tickets for this event"
            }