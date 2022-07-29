
from db.init_db import InitDB
import sqlalchemy as db
from sqlalchemy import and_
import json


class SearchDB:
    def __init__(self):
        self.temp_db = InitDB()

    