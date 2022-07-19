'''
Written by: Group 404
For COMP9900 Project 7 Event Management System

This file is the entry point for the flask application which will reveive JSON requests from the front end

To run the applicaiton:
$ flask run

This file performs the below in order:
1. Call db_main() function in the init_db.py file
    This will create a DB if it does not exist and load it full of data
2. Initialise a Flask instance and start it running
    This will be where the front end sends requests for data to
3. Define a number of resources which are located in apihandler.py 
    These resources can make queries on the database and return the data to the front end

'''

from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from api.apihandler import Test, Register, Events, Login, User, UserDetails, UserSensitiveDetails, UserChangePassword, Event, Create, Filter
from db.init_db import db_main

# Run db_main() in the init_db.py file to create the DB and fill it with data
db_main()

# Create a Flask object and define api as the main entry point for the application
app = Flask(__name__, static_url_path='', static_folder='frontend/build')
# Yunran: since we are not deploying we need to have CORS
CORS(app, supports_credentials=True)
api = Api(app)

# Matches URLs to resources defined in apihandler.py
api.add_resource(Test, '/test')
api.add_resource(Register, '/register')
api.add_resource(Events, '/events')
api.add_resource(Login, '/login')
api.add_resource(User, '/user', endpoint='user')
api.add_resource(UserDetails, '/user/details')
api.add_resource(UserSensitiveDetails, '/user/sensitive_details')
api.add_resource(UserChangePassword, '/user/login_credentials')
api.add_resource(Event, '/event')
api.add_resource(Create, '/create')
api.add_resource(Filter, '/filter')
