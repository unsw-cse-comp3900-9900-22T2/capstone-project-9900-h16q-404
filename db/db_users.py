

from db.init_db import InitDB
import sqlalchemy as db

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