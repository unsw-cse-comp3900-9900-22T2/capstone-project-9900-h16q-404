
from db.init_db import InitDB
import sqlalchemy as db

class TokenHandlerDB:
    def __init__(self):
        self.temp_db = InitDB()

    def get_host_id_from_token(self, token):
        check_query = db.select([self.temp_db.users]).where(self.temp_db.users.c.token == token)
        check_result = self.temp_db.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})
        list_result = check_result['result']
        if len(list_result) > 1:
            return "Error - more than one user with this token"
        else:
            return list_result[0]['id']

    def get_host_username_from_token(self, token):
        check_query = db.select([self.temp_db.users]).where(self.temp_db.users.c.token == token)
        check_result = self.temp_db.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})
        list_result = check_result['result']
        if len(list_result) > 1:
            return "Error - more than one user with this token"
        else:
            return list_result[0]['username']

    def get_host_username_from_token(self, token):
        check_query = db.select([self.temp_db.users]).where(self.temp_db.users.c.token == token)
        check_result = self.temp_db.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})
        list_result = check_result['result']
        if len(list_result) > 1:
            return "Error - more than one user with this token"
        else:
            return list_result[0]['username']