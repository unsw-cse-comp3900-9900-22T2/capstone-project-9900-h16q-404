'''
Written by: Group 404

This file handles the API requests for getting reserved ticket information for a user

'''

from flask_restful import Resource, reqparse
from db.init_db import InitDB


class MyTickets(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        args = parser.parse_args()
        # assign variables
        token = args['token']

        # create db engine
        temp_db = InitDB()
        user_id = temp_db.get_host_id_from_token(token)
        result = temp_db.select_all_tickets(user_id)
        if len(result['result']) > 0:
            for i in result['result']:
                start_date, start_time, event_name = temp_db.get_event_time_date(i['event_id'])
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