"""
Functions:
# get/select
- get_user_record
- get_user_record_byname
# create/insert
- insert_users
- register_new_user
# update
- update_user_details
# delete
# helper
- get_new_user_id
- check_user_exists
- check_userid_exists
- check_passwords_match
"""

# import third party libaries
import sqlalchemy as db
from sqlalchemy import and_


class UsersDB:
    def __init__(self):
        from app import databaseTables

        self.temp_db = databaseTables

    # Functions for selecting/getting user data

    def get_user_record(self, userid):
        user_query = db.select([self.temp_db.users]).where(
            self.temp_db.users.c.id == userid
        )
        user_result = self.temp_db.engine.execute(user_query).fetchall()

        if len(user_result) > 0:
            return user_result
        else:
            return -1

    def get_user_record_byname(self, username):
        user_query = db.select([self.temp_db.users]).where(
            self.temp_db.users.c.username == username
        )
        user_result = self.temp_db.engine.execute(user_query).fetchall()

        if len(user_result) > 0:
            return user_result
        else:
            return -1

    # Functions for inserting into the Users table

    def register_new_user(self, username, password):

        data = {
            "id": self.get_new_user_id(),
            "username": username,
            "password": password,
            "token": username,
            "email": username,
        }

        try:
            new_id = self.insert_users(data, False)
            return new_id
        except BaseException:
            return -1

    def insert_users(self, data, dummy):

        insert_check = self.check_userid_exists(data["id"])

        if insert_check == False:
            query = db.insert(self.temp_db.users).values(
                id=data["id"],
                username=data["username"],
                password=data["password"],
                token=data["token"],
                email=data["email"],
            )

            try:
                return self.temp_db.engine.execute(query).inserted_primary_key

            except BaseException:
                return -1
        else:
            print(
                "Item "
                + str(data["username"])
                + " not added to user table as it failed the insert check"
            )

    # Functions for updating rows in the Users table

    def update_user_details(self, params, token):
        update_query = (
            self.temp_db.users.update()
            .values(params)
            .where(self.temp_db.users.c.token == token)
        )

        try:
            return self.temp_db.engine.execute(update_query)
        except BaseException:
            return -1

    # Helper functions

    def check_user_exists(self, username):
        user_exists = False
        check_query = db.select([self.temp_db.users]).where(
            self.temp_db.users.c.username == username
        )
        check_result = self.temp_db.engine.execute(check_query).fetchall()

        if len(check_result) > 0:
            user_exists = True
        return user_exists

    def check_passwords_match(self, username, password):
        passwords_match = False
        check_query = db.select([self.temp_db.users]).where(
            and_(
                self.temp_db.users.c.username == username,
                self.temp_db.users.c.password == password,
            )
        )
        check_result = self.temp_db.engine.execute(check_query).fetchall()

        if len(check_result) > 0:
            passwords_match = True

        return passwords_match

    def check_userid_exists(self, userid):
        user_exists = False
        check_query = db.select([self.temp_db.users]).where(
            self.temp_db.users.c.id == userid
        )
        check_result = self.temp_db.engine.execute(check_query).fetchall()

        if len(check_result) > 0:
            user_exists = True
        return user_exists

    def get_new_user_id(self):
        # returns the highest id in the user table plus 1
        query_max_id = db.select([db.func.max(self.temp_db.users.columns.id)])
        max_id = self.temp_db.engine.execute(query_max_id).scalar()
        return max_id + 1
