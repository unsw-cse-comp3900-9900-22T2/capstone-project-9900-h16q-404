"""
Written by: Group 404
For COMP9900 Project 7 Event Management System

This file is the entry point for the flask application which will reveive JSON requests from the front end

This file performs the below in order:
1. Import all third party libraries required and then the custom classes made by Group 404
2. Call db_main() function in the init_db.py file
    This will create a DB if it does not exist and load it full of data
3. Initialise a Flask instance and start it running
    This will be where the front end sends requests for data to
4. Define a number of resources which are located in apihandler.py
    These resources can make queries on the database and return the data to the front end

To run the applicaiton:
$ flask run

"""

import nltk
nltk.download('stopwords')
nltk.download('punkt')

from sentence_transformers import SentenceTransformer
sentence_model = SentenceTransformer('distilbert-base-nli-mean-tokens')

# import database class
from api.recommendations import Recommendations
from db.init_db import db_main

# import login and register classes
from api.register import Register
from api.login import Login

# import all user-based classes
from api.user import User
from api.user_details import UserDetails
from api.user_change_password import UserChangePassword
from api.user_sensitive_details import UserSensitiveDetails

# import all events-based classes
from api.events import Events
from api.event import Event
from api.create import Create

# import classes used for landing page features
from api.filter import Filter
from api.search_event import SearchEvent

# import the tickets-based classes
from api.buy_tickets import BuyTickets
from api.my_tickets import MyTickets

# import the follow-based classes
from api.follow import Follow

# import the watchlist-based classes
from api.my_watchlist import MyWatchlist
from api.watched_events import WatchedEvents

# import the reviews-based classes
from api.reviews import Reviews
from api.host_replies import HostReplies

# import the ratings-based classes
from api.event_ratings import EventRatings
from api.user_ratings import UserRatings

# import the broadcast class
from api.broadcast import Broadcast

# import the recommendations class
from api.recommendations import Recommendations

# import third party libraries
from flask import Flask
from flask_restful import Api
from flask_cors import CORS


# Run db_main() in the init_db.py file to create the DB and fill it with data
databaseTables = db_main()

# Create a Flask object and define api as the main entry point for the application
app = Flask(__name__, static_url_path="", static_folder="frontend/build")

# Since we are not deploying we need to have CORS
CORS(app, supports_credentials=True)

# create the Api object
api = Api(app)

# Matches URLs to resources defined in api folder
api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(Events, "/events")
api.add_resource(Event, "/event")
api.add_resource(Create, "/create")
api.add_resource(User, "/user", endpoint="user")
api.add_resource(UserDetails, "/user/details")
api.add_resource(UserSensitiveDetails, "/user/sensitive_details")
api.add_resource(UserChangePassword, "/user/login_credentials")
api.add_resource(BuyTickets, "/buytickets")
api.add_resource(MyTickets, "/mytickets")
api.add_resource(Filter, "/filter")
api.add_resource(SearchEvent, "/event/search")
api.add_resource(Follow, "/follow")
api.add_resource(MyWatchlist, "/mywatchlist")
api.add_resource(WatchedEvents, "/watchedevents")
api.add_resource(Reviews, '/reviews')
api.add_resource(HostReplies, '/hostreplies')
api.add_resource(EventRatings, '/eventratings')
api.add_resource(UserRatings, '/userratings')
api.add_resource(Broadcast, '/broadcast')
api.add_resource(Recommendations, '/recommend')