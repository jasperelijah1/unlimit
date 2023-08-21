# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:29:35 2019

@author: Suriya Prakash
"""
import time
import cv2
def read_code():
    
import pyrebase
config = {
  "apiKey": "AIzaSyDKZDZifcM1E9UTw_-iU6CZ1DBKj-YvMqo",
  "authDomain": "mine-53ab0.firebaseapp.com",
  "databaseURL": "https://mine-53ab0.firebaseio.com/",
  "storageBucket": "mine-53ab0.appspot.com",
  "serviceAccount": "serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
#data={'a':3}
all_user_ids = db.child("racks").child('a').shallow().get()
print([i for i in all_user_ids.val()])
