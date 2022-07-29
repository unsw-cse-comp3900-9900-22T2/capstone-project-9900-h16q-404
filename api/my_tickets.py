'''
Written by: Group 404

This file handles the API requests for getting reserved ticket information for a user

'''
# import third party libraries
from flask_restful import Resource, reqparse

# import custom classes used to interact with the DB
from db.db_tickets import TicketsDB
from db.db_tickets import TicketsDB
from db.db_events import EventsDB
from db.db_token_handler import TokenHandlerDB


class MyTickets(Resource):
    def get(self):

        # parse request
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        args = parser.parse_args()

        token = args['token']

        # create db engines
        tickets_db = TicketsDB()
        events_db = EventsDB()
        token_db = TokenHandlerDB()

        user_id = token_db.get_host_id_from_token(token)
        result = tickets_db.select_all_tickets(user_id)
        if len(result['result']) > 0:
            for i in result['result']:
                start_date, start_time, event_name = events_db.get_event_time_date(i['event_id'])
                i['start_date'] = start_date
                i['start_time'] = start_time
                i['event_name'] = event_name
            return {
                'resultStatus': 'SUCCESS',
                'result': result
            }

        else:
            return {
                'resultStatus': 'ERROR',
                'message': 'No tickets found for this user'
            }