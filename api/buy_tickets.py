'''
Written by: Group 404

This file handles the API requests for getting ticket information, reserving tickets and unreserving tickets 

'''
# import third party libaries
from flask_restful import Resource, reqparse

# import custom classes used to interact with the DB
from db.db_tickets import TicketsDB
from db.db_token_handler import TokenHandlerDB


class BuyTickets(Resource):
    def get(self):

        # parse request
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='args')
        parser.add_argument('event_id', type=int, location='args')
        args = parser.parse_args()

        token = args['token']
        event_id = args['event_id']

        # create db engine
        temp_db = TicketsDB()

        result = temp_db.select_tickets_event_id(event_id)

        if len(result['result']) == 0:
            return {
                'resultStatus': 'ERROR',
                'message': 'no tickets for this event exist'                
            }

        return {
            'resultStatus': 'SUCCESS',
            'message': result
        }

    def post(self):

        token, tickets = self.parse_request()

        # create db engine
        token_db, tickets_db = self.gen_db_engines()

        # need to convert token to user_id
        user_id = token_db.get_host_id_from_token(token)
        failed = []
        
        for i in tickets:
            try:
                tickets_db.reserve_tickets(i, user_id)
            except:
                failed.append(i)
        if len(failed) > 0:
            return{
                'resultStatus': 'ERROR',
                'message': failed
            }
        else:
            return {
                'resultStatus': 'SUCCESS',
                'message': 'Tickets successfully booked'
            }

    def put(self):

        token, tickets = self.parse_request()

        # create db engine
        token_db, tickets_db = self.gen_db_engines()

        # need to convert token to user_id
        user_id = token_db.get_host_id_from_token(token)
        failed = []

        for i in tickets:
            try:
                tickets_db.refund_tickets(i, user_id)
            except:
                failed.append(i)

        if len(failed) > 0:
            return{
                'resultStatus': 'ERROR',
                'message': failed
            }
        else:
            return {
                'resultStatus': 'SUCCESS',
                'message': 'Tickets successfully unreserved'
            }


    def parse_request(self):

        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        parser.add_argument('tickets', action='append')
        args = parser.parse_args()

        # assign variables
        token = args['token']
        tickets = args['tickets']

        return token, tickets

    def gen_db_engines():
        # create db engine
        token_db = TokenHandlerDB()
        tickets_db = TicketsDB()

        return token_db, tickets_db