# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 22:38:47 2021
@author: Gillies
"""

from google.cloud import ndb
from google.oauth2 import service_account
import json

# credentials
key_location = "hotaru-kanri-cb5b35d48401.json"
credentials = service_account.Credentials.from_service_account_file(key_location)

# build a cloud datastore client
ndbclient = ndb.Client(project="hotaru-kanri", credentials=credentials)

# ------------- google datastore storage-related functions and classes ------------------------
class sentence_pair(ndb.Model):
    source = ndb.StringProperty()
    target = ndb.StringProperty()
    s_sentence = ndb.StringProperty()
    t_sentence = ndb.StringProperty()
    b_or_k = ndb.StringProperty()
    category = ndb.StringProperty()
    associated_zuban = ndb.StringProperty()

    
# This creates one field.  It is filled by the crawler.
def create_sentence_pair(s, t, ss, ts, bk, cat, az):
    one = sentence_pair(
        id = s + "_" + t + "_" + bk + "_" + cat + "_" + ss,
        source = s,
        target = t,
        s_sentence = ss,
        t_sentence = ts,
        b_or_k = bk,
        category = cat,
        associated_zuban = az)
    one.put()

def get_or_put_sentence_pair(request):

    request_json = request.get_json(silent=True)
    request_args = request.args
    
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
    
        return ('', 204, headers)
    
    else:
   
        if request.args and 'get_or_put' in request.args:
            get_or_put = request.args.get('get_or_put')
            source = request.args.get('source')
            target = request.args.get('target')
            s_sentence = request_args.get('s_sentence')
            t_sentence = request_args.get('t_sentence')
            b_or_k = request.args.get('b_or_k')
            category = request.args.get('category')
            associated_zuban = request.args.get('associated_zuban')
        elif request_json and 'get_or_put' in request_json:
            get_or_put = request_json['get_or_put']
            source = request_json['source']
            target = request_json['target']
            s_sentence = request_json['s_sentence']
            t_sentence = request_json['t_sentence']
            b_or_k = request_json['b_or_k']
            category = request_json['category']
            associated_zuban = request_json['associated_zuban']
            
        headers = {
            'Access-Control-Allow-Origin': '*'
        }
        value = {
            "success": "No pairs found for that language pair",
            "contents": [''], 
        }
    
        if (get_or_put == "get"):
            
            with ndbclient.context():
            
                contentsToReturn = []
                
                query = sentence_pair.query().filter(sentence_pair.source == source, sentence_pair.target == target, sentence_pair.b_or_k == b_or_k, sentence_pair.category == category)
                results = list(query.fetch())
             
                for r in results:
                    contentsToReturn.append(r.s_sentence)
                    contentsToReturn.append(r.t_sentence)
                        
            value["success"] = "Returned sentence pairs (I think...)"
            value["contents"] = contentsToReturn

            
        if (get_or_put == "put"):
            
            added = 0
            edited = 0
    
            with ndbclient.context():
                
                for p in range(0, len(s_sentence)):
                    
                    # Let's assume that the sentence we're trying to put already
                    # exists in the database (meaning the source is already there)
                    # For example, maybe in the database we have
                    
                    #JP: 注意 
                    #EN: Caution
                    
                    # But now, we're trying to put
                    
                    #JP: 注意
                    #EN: WARNING
                    
                    # In such a case, we should notice that the source is the same
                    # and then overwrite the target.  The main idea being that
                    # WE DON'T WANT ANY SEGMENTS WITH THE SAME SOURCE IN THE DB
                    
                    try:
                        thisKey = source + "_" + target + "_" + b_or_k + "_" + category + "_" + s_sentence[p]
                        entity = ndb.Key(sentence_pair, thisKey).get()
                    
                        if (entity.t_sentence != t_sentence[p]):
                            entity.t_sentence = t_sentence[p]
                            entity.associated_zuban = associated_zuban
                            entity.put()
                            edited = edited + 1
                           
                            
                            
                        
                    except:
                        create_sentence_pair(source, target, s_sentence[p], t_sentence[p], b_or_k, category, associated_zuban)
                        added = added + 1
                
                value["success"] = "Added " + str(added) + " sentences, and edited " + str(edited)
                
              
    returnPackage = json.dumps(value)

    return (returnPackage, 200, headers)