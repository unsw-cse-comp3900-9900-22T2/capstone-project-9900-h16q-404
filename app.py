from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
#from flask_cors import CORS #comment this on deployment
from api.apihandler import ApiHandler, SignUp, Events
from db.init_db import db_main

db_main()

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
#CORS(app) #comment this on deployment
api = Api(app)

api.add_resource(ApiHandler, '/flask/hello')

api.add_resource(SignUp, '/signup')

api.add_resource(Events, '/events')

# print(db.select(5))