'''
Written by: Group 404
For COMP9900 Project 7 Event Management System

This file defines the Resources that connect the front end URLs to the backend which will call the database.

'''

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask_restful import Resource, reqparse
from flask import request
from db.init_db import InitDB
from datetime import datetime, timedelta
from collections import defaultdict
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class Register(Resource):
    def get(self):
        return {
            'resultStatus': 'SUCCESS',
            'message': "Hello This is Sign Up response"
        }

    def post(self): 
        # If a post request is sent to /register

        # parse request
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('confirm', type=str)
        args = parser.parse_args()

        # get email and password
        request_email = args['email']
        request_password = args['password']

        temp_db = InitDB()
        # check user exists
        user_exists = temp_db.check_user_exists(request_email)

        # if user does not exists return error
        if user_exists == True:
            return {"status": "Error", "message": "User already exists"}
            

        # TODO here:
        # if user does not exists, store password and username
        new_id = temp_db.register_new_user(request_email, request_password)
        if new_id == -1:
            return {"status": "Error", "message": "could not register new user"}
        else:
            final_ret = {"status": "Success", "message": "new user registerd with id = " +str(new_id)}

        return final_ret

class Test(Resource):
    def get(self):
        return {
            'resultStatus': 'SUCCESS',
            'message': "Hello Api Handler"
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("type", type=str)
        parser.add_argument("message", type=str)
        args = parser.parse_args()

        # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')
        request_type = args['type']
        request_json = args['message']
        # ret_status, ret_msg = ReturnData(request_type, request_json)
        # currently just returning the req straight
        ret_status = request_type
        ret_msg = request_json

        if ret_msg:
            message = "Your Message Requested: {}".format(ret_msg)
        else:
            message = "No Msg"
    
        final_ret = {"status": "Success", "message": message}

        return final_ret

class Events(Resource):
    def get(self):
        temp_db = InitDB()
        result = temp_db.select_all_events()

        return {
            'resultStatus': 'SUCCESS',
            'message': result
        }

class Login(Resource):
    def post(self):

        # parse request
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        # get email and password
        request_username = args['username']
        request_password = args['password']

        temp_db = InitDB()
        user_exists = temp_db.check_user_exists(request_username)
        
        if user_exists == False:
            return {"status": "Error", "message": "User does not exists"}

        # if user does exist, check passwords match
        if user_exists == True:
            passwords_match = temp_db.check_passwords_match(request_username, request_password)
        
        if passwords_match == False:
            return {"status": "Error", "message": "Password is incorrect"}
        
        user_record = temp_db.get_user_record_byname(request_username)
        result_dict = {}
        result_dict['userId'] = user_record[0][0]
        result_dict['email'] = user_record[0][4]
        result_dict['firstname'] = user_record[0][5]
        result_dict['lastname'] = user_record[0][6]
        
        # check dob not none then convert to string
        dob = user_record[0][7]
        result_dict['dateOfBirth'] = dob
        if dob is not None:
            result_dict['dateOfBirth'] = dob.strftime("%Y-%m-%d")
        
        result_dict['gender'] = user_record[0][8]
        result_dict['phone'] = user_record[0][9]
        result_dict['vac'] = user_record[0][10]

        return {
            'resultStatus': 'SUCCESS',
            'message': result_dict
        }


class User(Resource):
    def get(self):
        # parse request
        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=int, location='args')
        args = parser.parse_args()

        request_userId = args['userId']

        temp_db = InitDB()
        user_exists = temp_db.check_userid_exists(request_userId)
        
        if (user_exists == False):
            return {"status": "Error", "message": "User does not exists"}
        
        user_record = temp_db.get_user_record(request_userId)
        result_dict = {}
        result_dict['userId'] = user_record[0][0]
        result_dict['email'] = user_record[0][4]
        result_dict['firstname'] = user_record[0][5]
        result_dict['lastname'] = user_record[0][6]
        
        # check dob not none then convert to string
        dob = user_record[0][7]
        result_dict['dateOfBirth'] = dob
        if dob is not None:
            result_dict['dateOfBirth'] = dob.strftime("%Y-%m-%d")
        
        result_dict['gender'] = user_record[0][8]
        result_dict['phone'] = user_record[0][9]
        result_dict['vac'] = user_record[0][10]
        
        # Get events hosted by this user
        result_dict['events'] = []
        user_events = temp_db.select_events_hostid(request_userId)
        if (len(user_events) > 0):
            event_list = []
            for event in user_events:
                event_list.append({"id":event['id'], "name":event['event_name'], "startDate":event['start_date']})
                #event_list.append([event['id']])
            result_dict['events'] = event_list
        
        return {
            'resultStatus': 'SUCCESS',
            'message': result_dict
        }

class UserDetails(Resource):
    def patch(self):
        temp_db = InitDB()
        getRequest = request.json
        if ('token' in getRequest):
            user_token = request.json['token']
        else:
            return {"status": "Error", "message": "User Token was not Sent"}
        
        user_exists = temp_db.check_usertoken_exists(user_token)
        
        if (user_exists == False):
            return {"status": "Error", "message": "User does not exists"}
        
        user_details_params = {}
        
        if ('firstName' in getRequest):
            user_details_params['firstName'] = request.json['firstName']
        
        if ('lastName' in getRequest):
            user_details_params['lastName'] = request.json['lastName']
        
        if ('phone' in getRequest):
            user_details_params['phone'] = request.json['phone']
        
        if user_details_params:
            update_status = temp_db.update_user_details(user_details_params, user_token)
        else:
            update_status = 0
        
        if (update_status == -1):
            return {"status": "Error", "message": "Update Failed! Try Again!"}
        
        return {
            'resultStatus': 'SUCCESS',
            'message': "User Details Updated!"
        }

class UserSensitiveDetails(Resource):
    def patch(self):
        temp_db = InitDB()
        getRequest = request.json
        if ('token' in getRequest):
            user_token = request.json['token']
        else:
            return {"status": "Error", "message": "User Token was not Sent"}
            
        user_exists = temp_db.check_usertoken_exists(user_token)
        
        if (user_exists == False):
            return {"status": "Error", "message": "User does not exists"}
        
        user_details_params = {}
        
        if ('dateOfBirth' in getRequest):
            dob = datetime.strptime(request.json['dateOfBirth'], '%Y-%m-%d')
            user_details_params['dateOfBirth'] = dob
        
        if ('gender' in getRequest):
            user_details_params['gender'] = request.json['gender']
        
        if ('vaccinated' in getRequest):
            user_details_params['vaccinated'] = request.json['vaccinated']
        
        if user_details_params:
            update_status = temp_db.update_user_details(user_details_params, user_token)
        else:
            update_status = 0
        
        if (update_status == -1):
            return {"status": "Error", "message": "Update Failed! Try Again!"}
        
        return {
            'resultStatus': 'SUCCESS',
            'message': "Sensitive Details Updated!"
        }

class UserChangePassword(Resource):
    def patch(self):
        temp_db = InitDB()
        getRequest = request.json
        if ('token' in getRequest):
            user_token = request.json['token']
        else:
            return {"status": "Error", "message": "User Token was not Sent"}
        
        user_exists = temp_db.check_usertoken_exists(user_token)
        
        if (user_exists == False):
            return {"status": "Error", "message": "User does not exists"}

        # Yunran: Please include check old password here
        if ('old_password' in getRequest):
            old_password = request.json['old_password']
        else:
            return {"status": "Error", "message": "User Old Password was not Sent"}
        
        password_match = temp_db.check_passwords_match(user_token, old_password)
        if password_match == False:
            return {"status": "Error", "message": "Old password is not correct"}
        # Yunran: TODO: Please include update email here; can update email only or password only
        
        user_details_params = {}
        
        if ('new_email' in getRequest):
            user_details_params['email'] = request.json['new_email']
        
        if ('new_password' in getRequest):
            user_details_params['password'] = request.json['new_password']
        
        if user_details_params:
            update_status = temp_db.update_user_details(user_details_params, user_token)
        else:
            update_status = 0
        
        if (update_status == -1):
            return {"status": "Error", "message": "Update Failed! Try Again!"}
        
        return {
            'resultStatus': 'SUCCESS',
            'message': "User Password Successfully Reset!"
        }

class Event(Resource):
    def get(self):
        # parse the event_id and/or event_name arguments
        parser = reqparse.RequestParser()
        parser.add_argument('event_name', type=str, location="args")
        parser.add_argument('event_id', type=int, location="args")
        args = parser.parse_args()

        # assign variables
        event_name = args['event_name']
        event_id = args['event_id']

        # create db engine
        temp_db = InitDB()

        if event_id and event_name:
            # if both parameters are provided, return error
            return {
            'resultStatus': 'Error',
            'message': 'Both event ID and event name supplied, please supply only one'
            }
        elif event_name:
            # if event_name provided
            result = temp_db.select_event_name(event_name)
        elif event_id:
            # if event_id provided
            result = temp_db.select_event_id(event_id)
        else:
            # if neither event_id or event_name provided return error
            return {
            'resultStatus': 'Error',
            'message': 'Both event ID and event name were not supplied, please supply one'
            }

        if not result:
            return {
            'resultStatus': 'ERROR',
            'message': 'event not found'
        }

        # finally return result
        return {
            'resultStatus': 'SUCCESS',
            'event_details': result
        }

    def put(self):
        # parse the event_id and/or event_name arguments
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        parser.add_argument('detail', type=dict)
        parser.add_argument('event_id', type=str)
        args = parser.parse_args()

        # assign variables
        token = args['token']
        event_details = args['detail']
        event_id = args['event_id']



        # create db engine
        temp_db = InitDB()
        result = temp_db.update_event(event_id, event_details, token)
        if result == True:
            return {
            'resultStatus': 'SUCCESS',
            }
        else:
            return {
            'resultStatus': 'ERROR',
            } 




    def delete(self):
        # parse the event_id and/or event_name arguments
        parser = reqparse.RequestParser()
        parser.add_argument('event_name', type=str, location="args")
        parser.add_argument('event_id', type=int, location="args")
        args = parser.parse_args()

        # assign variables
        event_name = args['event_name']
        event_id = args['event_id']

        # create db engine
        temp_db = InitDB()

        if event_id and event_name:
            # if both parameters are provided, return error
            return {
            'resultStatus': 'Error',
            'message': 'Both event ID and event name supplied, please supply only one'
            }
        elif event_name:
            # if event_name provided
            result = temp_db.delete_event_name(event_name)
            event_details = event_name
        elif event_id:
            # if event_id provided
            result = temp_db.delete_event_id(event_id)
            event_details = event_id
        else:
            # if neither event_id or event_name provided return error
            return {
            'resultStatus': 'Error',
            'message': 'Both event ID and event name were not supplied, please supply one'
            }

        if result == True:
        # If result is True, return SUCCESS and event details
            return {
                'resultStatus': 'SUCCESS',
                'event': event_details,
                'message': 'event deleted'
            }

        if "Error" in result:
        # if result != True, return ERROR and error message
            return {
                'resultStatus': 'ERROR',
                'message': result
            }    

class Create(Resource):
    def post(self):
        # parse the event_id and/or event_name arguments
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        parser.add_argument('detail', type=dict)
        args = parser.parse_args()

        # assign variables
        token = args['token']
        event_details = args['detail']

        # create db engine
        temp_db = InitDB()

        try:
            new_id, insert_data = temp_db.create_event(token, event_details)
            insert_data['start_date'] = str(insert_data['start_date'])
            insert_data['start_time'] = str(insert_data['start_time'])[:-3]
            insert_data['end_date'] = str(insert_data['end_date'])
            insert_data['end_time'] = str(insert_data['end_time'])[:-3]
            return {
                'resultStatus': 'SUCCESS',
                'new_event_id': new_id,
                'event_details': insert_data
            }
        except:
            return {
                'resultStatus': 'ERROR',
                'message': 'failed to insert new event into events table'
            }

class Filter(Resource):
    def get(self):
        # parse the event filter type arguments
        parser = reqparse.RequestParser()
        parser.add_argument('filterType', type=str, location="args")
        args = parser.parse_args()

        # assign variables
        filter_type = args['filterType']
        
        # create db engine
        temp_db = InitDB()
        
        # Get events hosted by this user
        result = temp_db.select_events_bytype(filter_type)
        
        if not result:
            return {
            'resultStatus': 'ERROR',
            'message': 'No Events Match Filter Type'
        }

        # finally return result
        return {
            'resultStatus': 'SUCCESS',
            'event_details': result
        }
class BuyTickets(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='args')
        parser.add_argument('event_id', type=int, location='args')
        args = parser.parse_args()

        # assign variables
        token = args['token']
        event_id = args['event_id']

        # create db engine
        temp_db = InitDB()
        result = temp_db.select_tickets_event_id(event_id)

        if len(result['result']) == 0:
            return {
                'resultStatus': 'ERROR',
                'message': 'no tickets for this event exist'                
            }

        return {
            'resultStatus': 'SUCCESS',
            'message': result
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        parser.add_argument('tickets', action='append')
        args = parser.parse_args()

        # assign variables
        token = args['token']
        tickets = args['tickets']

        # create db engine
        temp_db = InitDB()

        # need to convert token to user_id
        user_id = temp_db.get_host_id_from_token(token)
        failed = []
        for i in tickets:
            try:
                temp_db.reserve_tickets(i, user_id)
            except:
                failed.append(i)

        if len(failed) > 0:
            return{
                'resultStatus': 'ERROR',
                'message': failed
            }
        else:
            return {
                'resultStatus': 'SUCCESS',
                'message': 'Tickets successfully booked'
            }

    def put(self):

        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        parser.add_argument('tickets', action='append')
        args = parser.parse_args()

        # assign variables
        token = args['token']
        tickets = args['tickets']

        # create db engine
        temp_db = InitDB()

        # need to convert token to user_id
        user_id = temp_db.get_host_id_from_token(token)
        failed = []
        for i in tickets:
            try:
                temp_db.refund_tickets(i, user_id)
            except:
                failed.append(i)

        if len(failed) > 0:
            return{
                'resultStatus': 'ERROR',
                'message': failed
            }
        else:
            return {
                'resultStatus': 'SUCCESS',
                'message': 'Tickets successfully unreserved'
            }

class MyTickets(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        args = parser.parse_args()
        # assign variables
        token = args['token']

        # create db engine
        temp_db = InitDB()
        user_id = temp_db.get_host_id_from_token(token)
        result = temp_db.select_all_tickets(user_id)
        if len(result['result']) > 0:
            for i in result['result']:
                start_date, start_time, event_name = temp_db.get_event_time_date(i['event_id'])
                i['start_date'] = start_date
                i['start_time'] = start_time
                i['event_name'] = event_name
            return {
                'resultStatus': 'SUCCESS',
                'result': result
            }

        else:
            return {
                'resultStatus': 'ERROR',
                'message': 'No tickets found for this user'
            }
        
class SearchEvent(Resource):
    def post(self):
        getRequest = request.json
        if ('keyWordList' in getRequest):
            searchTerms = getRequest['keyWordList']
        else:
            return {"status": "Error", "message": "Search Key Word List was not Sent"}
        
        # create db engine
        temp_db = InitDB()
        
        allEvents = temp_db.select_all_events()
        result = []
        
        if (len(searchTerms) > 0):
            for event in allEvents:
                eventsStrToSearch = " ". join((event['event_name'], event['description'], event['type']))
                eventsStrToSearch = eventsStrToSearch.lower()
                queryinEvent = False
                for item in searchTerms:
                    if item in eventsStrToSearch:
                        queryinEvent = True
                        break;
                if queryinEvent:
                    result.append(event)
        
        return {
            'resultStatus': 'SUCCESS',
            'message': result
        } 

class Follow(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        parser.add_argument('target_id', type=str, location='args')
        args = parser.parse_args()
        
        # assign variables
        token = args['token']
        following_id = args['target_id']

        temp_db = InitDB()
        follower_id = temp_db.get_host_id_from_token(token)
        return temp_db.check_follower(follower_id, following_id)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        parser.add_argument('target_id', type=str)
        args = parser.parse_args()
        
        # assign variables
        token = args['token']
        following_id = args['target_id']

        temp_db = InitDB()
        follower_id = temp_db.get_host_id_from_token(token)

        return temp_db.add_follower(follower_id, following_id)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        parser.add_argument('target_id', type=str)
        args = parser.parse_args()
        
        # assign variables
        token = args['token']
        following_id = args['target_id']

        temp_db = InitDB()
        follower_id = temp_db.get_host_id_from_token(token)

        return temp_db.delete_follower(follower_id, following_id)

class MyWatchlist(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        args = parser.parse_args()
        
        # assign variables
        token = args['token']

        temp_db = InitDB()
        user_id = temp_db.get_host_id_from_token(token)

        all_following_ids = temp_db.get_all_following_user_ids(user_id)
        
        all_following_user_details = []

        for i in all_following_ids:
            user_record = temp_db.get_user_record(i['following'])
            if user_record != -1:
                all_following_user_details.append(user_record[0])

        return_users = []
        for i in all_following_user_details:
            user_dict = {}
            user_dict['user_id'] = i[0]
            user_dict['user_name'] = i[1]
            return_users.append(user_dict)

        return return_users


class WatchedEvents(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='headers')
        args = parser.parse_args()
        
        # assign variables
        token = args['token']

        temp_db = InitDB()
        user_id = temp_db.get_host_id_from_token(token)

        following_users = temp_db.get_all_following_user_ids(user_id)
        
        return_events = []
        for i in following_users:
            events = temp_db.select_events_hostid(i['following'])
            for j in events:
                return_events.append(j)

        return return_events
class Reviews(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='args')
        parser.add_argument('eventId', type=int, location='args')
        args = parser.parse_args()
        # assign variables
        token = args['token']
        eventId = args['eventId']

        # create db engine
        temp_db = InitDB()
        
        # check user exists
        user_exists = temp_db.check_usertoken_exists(token)
        
        #user_name = temp_db.get_host_username_from_token(token)
        
        
        #is_host = temp_db.check_user_isHost(user_id, eventId)
        #has_ticket = temp_db.check_user_hasTicket(user_id, eventId)
        #has_comment = temp_db.check_user_hasComment(user_id, eventId)
        
        result_dict = {}
        result_dict['hostedBy'] = temp_db.get_event_hostname(eventId)
        
        if user_exists:
            user_id = temp_db.get_host_id_from_token(token)
            result_dict['is_host'] = temp_db.check_user_isHost(user_id, eventId)
            result_dict['has_ticket'] = temp_db.check_user_hasTicket(user_id, eventId)
            result_dict['has_comment'] = temp_db.check_user_hasComment(user_id, eventId)
        else:
            result_dict['is_host'] = False
            result_dict['has_ticket'] = False
            result_dict['has_comment'] = False
        
        result_dict['reviews'] = []
        
        event_reviews = temp_db.get_reviews_by_eventId(eventId)
        if (len(event_reviews) > 0):
            review_list = []
            for review in event_reviews:
                review_list.append({"reviewedBy":temp_db.get_username_from_id(review['userId']),
                                    "review":review['review'],
                                    "reviewedOn":review['reviewTimeStamp'],
                                    "rating":review['rating'],
                                    "reply":review['reply'],
                                    "repliedOn":review['replyTimeStamp']
                                    })
                #event_list.append([event['id']])
            result_dict['reviews'] = review_list
        
        return {
            'resultStatus': 'SUCCESS',
            'message': result_dict
        }
    
    def post(self):
        # parse request
        getRequest = request.json
        if ('token' in getRequest):
            token = getRequest['token']
        else:
            return {"status": "Error", "message": "token was not Sent"}
        
        if ('eventId' in getRequest):
            eventId = getRequest['eventId']
        else:
            return {"status": "Error", "message": "Event Id was not Sent"}
        
        if ('timeStamp' in getRequest):
            timeStamp = getRequest['timeStamp']
        else:
            return {"status": "Error", "message": "Time Stamp was not Sent"}
        
        if ('comment' in getRequest):
            comment = getRequest['comment']
        else:
            comment = ""
        
        if ('rating' in getRequest):
            rating = getRequest['rating']
        
        
        temp_db = InitDB()
        
        # check user exists
        user_exists = temp_db.check_usertoken_exists(token)
        
        if user_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User Token does not match'
            }
        
        user_id = temp_db.get_host_id_from_token(token)
        
        # check event exists
        event_exists = temp_db.check_eventid_exists(eventId)
        if event_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'Event Id does not exist'
            }
        
        # get event host and type by id
        eventDetails = temp_db.select_event_byId(eventId)
        
        if (len(eventDetails) < 0):
            return {
                'resultStatus': 'ERROR',
                'message': 'Unable to Retreive Event Details'
            }
        
        host = eventDetails['host']
        eventType = eventDetails['type']
        
        new_id = temp_db.post_review(user_id, eventId, timeStamp, comment, rating, host, eventType)
        
        if new_id == -1:
            return {"status": "Error", "message": "Could not add review"}
        else:
            return {"status": "Success", "message": "Added Review Succesfully"}
        
    
    def patch(self):
        # parse request
        getRequest = request.json
        if ('token' in getRequest):
            token = getRequest['token']
        else:
            return {"status": "Error", "message": "token was not Sent"}
        
        if ('eventId' in getRequest):
            eventId = getRequest['eventId']
        else:
            return {"status": "Error", "message": "Event Id was not Sent"}
        
        user_reviews_params = {}
        
        if ('timeStamp' in getRequest):
            reviewedTime = datetime.strptime(getRequest['timeStamp'], '%Y-%m-%d %H:%M')
            user_reviews_params['reviewTimeStamp'] = reviewedTime
        
        if ('comment' in getRequest):
            user_reviews_params['review'] = getRequest['comment']
        
        if ('rating' in getRequest):
            user_reviews_params['rating'] = getRequest['rating']
        
        temp_db = InitDB()
        
        # check user exists
        user_exists = temp_db.check_usertoken_exists(token)
        
        if user_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User Token does not match'
            }
        
        user_id = temp_db.get_host_id_from_token(token)
        
        user_has_reviewed = temp_db.check_user_hasComment(user_id, eventId)
        
        if user_has_reviewed == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User has not reviewed before'
            }
        
        
        new_id = temp_db.update_user_reviews(user_reviews_params, user_id, eventId)
        
        if new_id == -1:
            return {"status": "Error", "message": "Could not update review!"}
        else:
            return {"status": "Success", "message": "Updated Review Succesfully"}
    
    def delete(self):
        # parse request
        getRequest = request.json
        if ('token' in getRequest):
            token = getRequest['token']
        else:
            return {"status": "Error", "message": "token was not Sent"}
        
        if ('eventId' in getRequest):
            eventId = getRequest['eventId']
        else:
            return {"status": "Error", "message": "Event Id was not Sent"}
        
        temp_db = InitDB()
        
        # check user exists
        user_exists = temp_db.check_usertoken_exists(token)
        
        if user_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User Token does not match'
            }
        
        user_id = temp_db.get_host_id_from_token(token)
        
        user_has_reviewed = temp_db.check_user_hasComment(user_id, eventId)
        
        if user_has_reviewed == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User has not reviewed before!'
            }
        
        new_id = temp_db.delete_user_reviews(user_id, eventId)
        
        if new_id == -1:
            return {"status": "Error", "message": "Could not delete review"}
        else:
            return {"status": "Success", "message": "Deleted Review Succesfully"}
        
class HostReplies(Resource):
    def patch(self):
        getRequest = request.json
        if ('token' in getRequest):
            token = getRequest['token']
        else:
            return {"status": "Error", "message": "token was not Sent"}
            
        if ('eventId' in getRequest):
            eventId = getRequest['eventId']
        else:
            return {"status": "Error", "message": "Event Id was not Sent"}
        
        if ('targetUserId' in getRequest):
            targetUserId = getRequest['targetUserId']
        else:
            return {"status": "Error", "message": "Target User Id was not Sent"}
        
        host_replies_params = {}
        
        if ('timeStamp' in getRequest):
            repliedTime = datetime.strptime(getRequest['timeStamp'], '%Y-%m-%d %H:%M')
            host_replies_params['replyTimeStamp'] = repliedTime
        
        if ('reply' in getRequest):
            host_replies_params['reply'] = getRequest['reply']
        
        temp_db = InitDB()
        
        # check user exists
        user_exists = temp_db.check_usertoken_exists(token)
        
        if user_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User Token does not match'
            }
        
        user_id = temp_db.get_host_id_from_token(token)
        
        user_has_reviewed = temp_db.check_user_hasComment(targetUserId, eventId)
        
        if user_has_reviewed == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User has not reviewed before'
            }
        
        new_id = temp_db.update_user_reviews(host_replies_params, targetUserId, eventId)
        
        if new_id == -1:
            return {"status": "Error", "message": "Could not update reply!"}
        else:
            return {"status": "Success", "message": "Updated Reply Succesfully"}
        
    def delete(self):
        getRequest = request.json
        if ('token' in getRequest):
            token = getRequest['token']
        else:
            return {"status": "Error", "message": "token was not Sent"}
            
        if ('eventId' in getRequest):
            eventId = getRequest['eventId']
        else:
            return {"status": "Error", "message": "Event Id was not Sent"}
        
        if ('targetUserId' in getRequest):
            targetUserId = getRequest['targetUserId']
        else:
            return {"status": "Error", "message": "Target User Id was not Sent"}
        
        host_replies_delete_params = {}
        host_replies_delete_params['replyTimeStamp'] = None
        host_replies_delete_params['reply'] = ""
        
        temp_db = InitDB()
        
        # check user exists
        user_exists = temp_db.check_usertoken_exists(token)
        
        if user_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User Token does not match'
            }
        
        user_id = temp_db.get_host_id_from_token(token)
        
        user_has_reviewed = temp_db.check_user_hasComment(targetUserId, eventId)
        
        if user_has_reviewed == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'User has not reviewed before'
            }
        
        new_id = temp_db.update_user_reviews(host_replies_delete_params, targetUserId, eventId)
        
        if new_id == -1:
            return {"status": "Error", "message": "Could not delete reply!"}
        else:
            return {"status": "Success", "message": "Deleted Reply Succesfully"}


class EventRatings(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='args')
        parser.add_argument('eventId', type=int, location='args')
        args = parser.parse_args()
        # assign variables
        token = args['token']
        eventId = args['eventId']

        # create db engine
        temp_db = InitDB()
        
        # check user exists
        user_exists = temp_db.check_usertoken_exists(token)
        
        # check event exists
        event_exists = temp_db.check_eventid_exists(eventId)
        if event_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'Event Id does not exist'
            }
        
        # get event host and type by id
        eventDetails = temp_db.select_event_byId(eventId)
        
        if (len(eventDetails) < 0):
            return {
                'resultStatus': 'ERROR',
                'message': 'Unable to Retreive Event Details'
            }
        
        host = eventDetails[0]['host']
        eventType = eventDetails[0]['type']
        hostName = eventDetails[0]['host_username']
        
        result_dict = {}
        result_dict['Host Name'] = hostName
        result_dict['Event Type'] = eventType
        
        # get ratings based on host and event type
        eventRatings = temp_db.select_ratings_from_reviews(host, eventType)
        numRatings = len(eventRatings)
        
        # Compute Average Rating
        average_rating = 0
        
        if (len(eventRatings) > 0):
            sum_ratings = 0
            for rating in eventRatings:
                sum_ratings += rating['rating']
            average_rating = sum_ratings / numRatings
        
        result_dict['Average Rating'] = round(average_rating, 2)
        
        return {
            'resultStatus': 'SUCCESS',
            'message': result_dict
        }
        
class UserRatings(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=int, location='args')
        args = parser.parse_args()
    
        # assign variables
        userId = args['userId']
        
        # create db engine
        temp_db = InitDB()
        
        user_ratings = temp_db.select_ratings_by_host(userId)
        numEvents = len(user_ratings)
        overall_rating = 0
        
        result_dict = {}
        event_type_rating_dict = defaultdict(float)
        event_type_count_dict = defaultdict(int)
        
        if (numEvents > 0):
            sum_ratings = 0
            for rating in user_ratings:
                sum_ratings += rating['rating']
                event_type_rating_dict[rating['eventType']] += rating['rating']
                event_type_count_dict[rating['eventType']] += 1
            overall_rating = sum_ratings / numEvents
        
        
        for key, val in event_type_rating_dict.items():
            temp = event_type_rating_dict[key]
            newVal = temp / event_type_count_dict[key]
            event_type_rating_dict[key] = round(newVal, 2)

        result_dict['Overall Rating'] = round(overall_rating, 2)
        result_dict['Event Type Rating'] = event_type_rating_dict
        
        return {
            'resultStatus': 'SUCCESS',
            'message': result_dict
        }

class Broadcast(Resource):
    def post(self):
        getRequest = request.json
        if ('eventId' in getRequest):
            eventId = getRequest['eventId']
        else:
            return {"status": "Error", "message": "Event Id was not Sent"}
        
        if ('msg' in getRequest):
            messageToBroadcast = getRequest['msg']
        else:
            return {"status": "Error", "message": "msg was not Sent"}
        
        # create db engine
        temp_db = InitDB()
        
        # post message to broadcast table
        new_id = temp_db.post_broadcast(eventId, messageToBroadcast)
        
        # get email of all users who have tickets to eventId
        get_users = temp_db.get_alluser_record()
        users_dict = {}
        
        if (len(get_users) > 0):
            for user in get_users:
                get_name = user['username'].split('@')[0].replace("."," ").title()
                users_dict[user['id']] = (user['username'], get_name)
        
        # fetch all user id from tickets for eventId
        user_has_tickets = temp_db.get_userid_with_tickets(eventId)
        user_mail_list = []
        
        if (len(user_has_tickets) > 0):
            for user in user_has_tickets:
                user_mail_list.append(users_dict[user])

        to_emails = user_mail_list
        sender_email = os.environ.get('MAIL_DEFAULT_SENDER')
        sender_name = os.environ.get('MAIL_SENDER_NAME')

        message = Mail(
        from_email=(sender_email, sender_name),
        subject='Hello',
        plain_text_content=messageToBroadcast,
        to_emails=to_emails,
        is_multiple=True)
        
        try:
            sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sendgrid_client.send(message)
        except Exception as e:
            return {"status": "Error", "message": "Error broadcasting message to ticket holders"}
        
        return {
            'resultStatus': 'SUCCESS',
            'message': "Successfully broadcasted email to all ticket holders for this event"
        }
        

class Recommendations(Resource):    
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='args')
        args = parser.parse_args()
        
        token = args['token']
        
        # create db engine
        temp_db = InitDB()
        
        # check user exists
        token_exists = temp_db.check_usertoken_exists(token)
        
        if token_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'Token does not exist'
            }
        
        # get user id from token
        user_id = temp_db.get_host_id_from_token(token)
        username = temp_db.get_host_username_from_token(token)
        
        # get event id of from events the user had attended using tickets table
        events_booked = temp_db.get_eventid_with_tickets(user_id)
        
        # Now for all event id, get event type description and host
        attended_event_type = set()
        attended_event_host = set()
        attended_event_description = set()
        
        current_day = datetime.now()
        
        for event in events_booked:
            get_event = temp_db.select_event_byId(event)[0]
            
            event_end_time = get_event['end_date'] + " " + get_event['end_time'];
            event_time_stamp = datetime.strptime(event_end_time, "%Y-%m-%d %H:%M:%S")
            
            # get data only from past events i.e. before today
            if (event_time_stamp < current_day):
                attended_event_type.add(get_event['type'])
                if (get_event['host_username'] != username):
                    attended_event_host.add(get_event['host_username'])
                attended_event_description.add(get_event['description'].lower())
        
        attended_event_description = list(attended_event_description)
        
        recommended_events = {}
        recommended_eventids = set()
        # find the recommended event in future by type
        recommended_eventid_bytype = temp_db.get_recommend_event_bytype(attended_event_type)
        # print(recommended_eventid_bytype)
        
        # find the recommended event in future by host
        recommended_eventid_byhost = temp_db.get_recommend_event_byhost(attended_event_host)
        # print(recommended_eventid_byhost)
        
        # find the recommended event by similarity in description
        future_events = temp_db.get_future_events()
        future_event_description = []
        future_event_id = []
        
        for i in range(len(future_events)):
            get_eventId = future_events[i]['id']
            get_eventdesc = future_events[i]['description']
            future_event_description.append(get_eventdesc.lower());
            future_event_id.append(get_eventId)
        
        
        stop_words = set(stopwords.words('english'))
        
        for event in range(len(attended_event_description)):
            word_tokens = word_tokenize(attended_event_description[event]);
            attended_event_description[event] = [w for w in word_tokens if not w.lower() in stop_words]
        
        for event in range(len(future_event_description)):
            word_tokens = word_tokenize(future_event_description[event]);
            future_event_description[event] = [w for w in word_tokens if not w.lower() in stop_words]
        
        recommended_eventid_bydesc = set()
        
        for attended_event in range(len(attended_event_description)):
            for future_event in range(len(future_event_description)):
                get_score = self.get_similarity_score(attended_event_description[attended_event],
                                                 future_event_description[future_event])
                # print(get_score)
                if (get_score >= 0.4):
                    recommended_eventid_bydesc.add(future_event_id[future_event])
        
        # print(recommended_eventid_bydesc)
        
        recommended_eventids = list(recommended_eventid_bytype | recommended_eventid_byhost | recommended_eventid_bydesc)
        
        recommended_events = []
        
        for event in range(len(future_events)):
            get_eventId = future_events[event]['id']
            if get_eventId in recommended_eventids:
                recommended_events.append(future_events[event])
                
        
        return {
            'resultStatus': 'SUCCESS',
            'message': recommended_events
        }
        

    def get_similarity_score(self,sentence1, sentence2):
            from sentence_transformers import SentenceTransformer
            from scipy.spatial import distance
            model = SentenceTransformer('distilbert-base-nli-mean-tokens')
            
            
            filtered_sentence1 = " ".join(sentence1)
            filtered_sentence2 = " ".join(sentence2)
            sentences = [filtered_sentence1, filtered_sentence2]
            sentence_embeddings = model.encode(sentences)

            # for sentence, embedding in zip(sentences, sentence_embeddings):
                # print("Sentence:", sentence)
                #print("Embedding:", embedding)
                #print("")
            
            
            return (1 - distance.cosine(sentence_embeddings[0], sentence_embeddings[1]))
    
