'''
Functions:
# get/select
- get_host_id_from_token
- get_host_username_from_token
# create/insert
# update
# delete
# helper
- check_usertoken_exists
'''


# import third party libraries
import sqlalchemy as db


class TokenHandlerDB:
    def __init__(self):
        from app import databaseTables
        self.temp_db = databaseTables

# Functions that select/get info from the DB

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

# Helper functions
    
    def check_usertoken_exists(self, usertoken):
        user_exists = False
        check_query = db.select([self.temp_db.users]).where(self.temp_db.users.c.token == usertoken)
        check_result = self.temp_db.engine.execute(check_query).fetchall()
        if len(check_result) > 0:
            user_exists = True
        return user_exists