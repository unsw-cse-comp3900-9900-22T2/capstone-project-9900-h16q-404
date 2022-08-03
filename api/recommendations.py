from flask_restful import Resource, reqparse
from flask import request
import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from db.db_token_handler import TokenHandlerDB
from db.db_recommendations import RecommendationsDB
from db.db_reviews import ReviewsDB


class Recommendations(Resource):    
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='args')
        args = parser.parse_args()
        
        token = args['token']
        
        # create db engine
        token_db = TokenHandlerDB()
        recommendations_db = RecommendationsDB()
        reviews_db = ReviewsDB()

        
        # check user exists
        token_exists = token_db.check_usertoken_exists(token)
        
        if token_exists == False:
            return {
                'resultStatus': 'ERROR',
                'message': 'Token does not exist'
            }
        
        # get user id from token
        user_id = token_db.get_host_id_from_token(token)
        username = token_db.get_host_username_from_token(token)
        
        # get event id of from events the user had attended using tickets table
        events_booked = recommendations_db.get_eventid_with_tickets(user_id)
        
        # Now for all event id, get event type description and host
        attended_event_type = set()
        attended_event_host = set()
        attended_event_description = set()
        
        current_day = datetime.datetime.now();
        
        for event in events_booked:
            try: 
                get_event = reviews_db.select_event_byId(event)[0]
                
                event_end_time = get_event['end_date'] + " " + get_event['end_time'];
                event_time_stamp = datetime.datetime.strptime(event_end_time, "%Y-%m-%d %H:%M:%S")
                
                # get data only from past events i.e. before today
                if (event_time_stamp < current_day):
                    attended_event_type.add(get_event['type'])
                    if (get_event['host_username'] != username):
                        attended_event_host.add(get_event['host_username'])
                    attended_event_description.add(get_event['description'].lower())
            except:
                pass
        
        attended_event_description = list(attended_event_description)
        
        recommended_events = {}
        recommended_eventids = set()
        # find the recommended event in future by type
        recommended_eventid_bytype = recommendations_db.get_recommend_event_bytype(attended_event_type)
        # print(recommended_eventid_bytype)
        
        # find the recommended event in future by host
        recommended_eventid_byhost = recommendations_db.get_recommend_event_byhost(attended_event_host)
        # print(recommended_eventid_byhost)
        
        # find the recommended event by similarity in description
        future_events = recommendations_db.get_future_events()
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