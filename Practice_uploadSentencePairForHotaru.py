# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 22:38:47 2021
@author: Gillies
"""

from google.cloud import ndb
from google.oauth2 import service_account
import json

# credentials
key_location = "hotaru-kanri-8434222bfa57.json"
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

def get_or_put_sentence_pair(get_or_put):
    
    value = {
        "success": "No pairs found for that language pair",
        "contents": [''], 
    }


    if (get_or_put == "get"):
        
        with ndbclient.context():
        
            contentsToReturn = []
            
            query = sentence_pair.query().filter(sentence_pair.source == "en-us", sentence_pair.target == "es-mx", sentence_pair.b_or_k == "B", sentence_pair.category == "AirConditionerInstallation")
            results = list(query.fetch())
            print(len(results))
            for r in results:
                contentsToReturn.append(r.s_sentence)
                contentsToReturn.append(r.t_sentence)

                    
        value["success"] = "Returned sentence pairs (I think...)"
        value["contents"] = "a"#contentsToReturn

        
    if (get_or_put == "put"):
        
        added = 0
        edited = 0
        s_sentence = ["From A", "Another from A", "This one is new"]
        t_sentence = ["A から", "これも A から編集", "新しい"]
        source = "en-us"
        target = "ja-jp"
        b_or_k = "B"
        category ="AirConditionerInstallation"
        associated_zuban = "editing just one and added one"

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
                        editedOne = True
                        
                        
                except:
                    if editedOne == False:
                        create_sentence_pair(source, target, s_sentence[p], t_sentence[p], b_or_k, category, associated_zuban)
                        added = added + 1
            
            value["success"] = "Added " + str(added) + " sentences, and edited " + str(edited)
            
          
    returnPackage = json.dumps(value)

    return returnPackage

print(get_or_put_sentence_pair("get"))
