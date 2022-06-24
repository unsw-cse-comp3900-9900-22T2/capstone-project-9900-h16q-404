'''
Written by: Group 404
For COMP9900 Project 7 Event Management System

This file is the entry point for the flask application which will reveive JSON requests from the front end

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
from api.apihandler import ApiHandler, SignUp, Events
from db.init_db import db_main

# Run db_main() in the init_db.py file to create the DB and fill it with data
db_main()

# Create a Flask object and define api as the main entry point for the application
app = Flask(__name__, static_url_path='', static_folder='frontend/build')
api = Api(app)

# Matches URLs to resources defined in apihandler.py
api.add_resource(ApiHandler, '/flask/hello')
api.add_resource(SignUp, '/signup')
api.add_resource(Events, '/events')