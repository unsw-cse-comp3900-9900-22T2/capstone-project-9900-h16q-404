

from db.init_db import InitDB
import sqlalchemy as db
from sqlalchemy import and_

class UsersDB:
    def __init__(self):
        self.temp_db = InitDB()

    def insert_users(self, data, dummy):
        insert_check = True
        check_query = db.select([self.temp_db.users]).where(self.temp_db.users.c.id == data["id"])
        check_result = self.temp_db.engine.execute(check_query)
        check_result = ({'result': [dict(row) for row in check_result]})
        for i in range(len(check_result['result'])):
             if data["id"] == (check_result["result"][i]['id']):
                insert_check = False
        
        # if no row exists with current primary key add new row
        if insert_check == True:
            if dummy == True:
                query = db.insert(self.temp_db.users).values(
                    id = data["id"],
                    username = data["username"],
                    password = data["password"],
                    token = data["token"],
                    email = data['username'],
                    dateOfBirth = data['dateOfBirth'],
                    vaccinated = data['vaccinated']
                )
            else:
                query = db.insert(self.temp_db.users).values(
                    id = data["id"],
                    username = data["username"],
                    password = data["password"],
                    token = data["token"],
                    email = data['username'],
                )
            try:
                result = self.temp_db.engine.execute(query).inserted_primary_key 
                return result 
            except:
                return -1
        else:
            print("Item " + str(data["username"]) + " not added to user table as it failed the insert check")

    def check_user_exists(self, username):
        user_exists = False
        check_query = db.select([self.temp_db.users]).where(self.temp_db.users.c.username == username)
        check_result = self.temp_db.engine.execute(check_query).fetchall()
        if len(check_result) > 0:
            user_exists = True
        return user_exists

    def register_new_user(self, username, password):
        # need to get new userID
        # function to get highest ID value

        data = {
            "id":self.temp_db.get_new_user_id(), 
            "username": username,
            "password": password,
            "token": username,
            "dateOfBirth": "",
            "vaccinated": ""
        }

        try:
            new_id = self.temp_db.insert_users(data, False)    
            return new_id
        except:
            return -1

    def check_passwords_match(self, username, password):
        passwords_match = False
        check_query = db.select([self.temp_db.users]).where(
            and_(
                self.temp_db.users.c.username == username,
                self.temp_db.users.c.password == password
                )
            )
        check_result = self.temp_db.engine.execute(check_query).fetchall()
        if len(check_result) > 0:
                passwords_match = True
        return passwords_match

    def get_user_record_byname(self, username):
        user_query = db.select([self.temp_db.users]).where(self.temp_db.users.c.username == username)
        user_result = self.temp_db.engine.execute(user_query).fetchall()
        if len(user_result) > 0:
            return user_result
        else:
            return -1

    def update_user_details(self, params, token):
        # update_query = self.users.update(). \
        # values({
        #     'phone': bindparam('phone'),
        #     'firstname': bindparam('firstname'),
        #     'lastname': bindparam('lastname')
        # }).where(self.users.c.token == token)
        # TODO: Ganesh can we delete all this stuff above^
        update_query = self.temp_db.users.update().values(params).where(self.temp_db.users.c.token == token)
        a = self.temp_db.engine.execute(update_query)
        # TODO: Ganesh this line is not required ^
        
        try:
            return self.temp_db.engine.execute(update_query)
        except:
            return -1

    def check_userid_exists(self, userid):
        user_exists = False
        check_query = db.select([self.temp_db.users]).where(self.temp_db.users.c.id == userid)
        check_result = self.temp_db.engine.execute(check_query).fetchall()
        if len(check_result) > 0:
            user_exists = True
        return user_exists

    def get_user_record(self, userid):
        user_query = db.select([self.temp_db.users]).where(self.temp_db.users.c.id == userid)
        user_result = self.temp_db.engine.execute(user_query).fetchall()
        if len(user_result) > 0:
            return user_result
        else:
            return -1