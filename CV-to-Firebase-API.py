"""
    OpenCV to Firebase Library

    Requires: pyrebase
    @user$ "pip(3) install pyrebase"

    SUMMARY
    > Contains functions for updating Firebase data with data generated from OpenCV Data

    > Data currently stored as JSON: {"avgIndex": 0, "lat": 0, "lng": 0}
        Note that some fields may currently be redundant and/or unecessary, need to determine use later

    Written by Austin Tsao
    August 12, 2020
"""

import pyrebase
import random

"""
Function: init
Initializes connection to Firebase
@param: None
@return: None
"""
def init():
    config = {
        "apiKey": "AIzaSyAf58ybK5T7_dZr10b4tum-XAu3aqu1v_Q",
        "authDomain": "social-distancing-monito-c9b2c.firebaseapp.com",
        "databaseURL": "https://social-distancing-monito-c9b2c.firebaseio.com",
        "projectId": "social-distancing-monito-c9b2c",
        "storageBucket": "social-distancing-monito-c9b2c.appspot.com",
        "messagingSenderId": "847811129335",
        "appId": "1:847811129335:web:505c7263ef941efeaf88f2",
        "measurementId": "G-H2DKQT2CK8"
    }

    firebase = pyrebase.initialize_app(config)
    global db
    db = firebase.database()

"""
Function: update
Updates index of camera at certain latitude and longitude in Firebase DB
@param
    lat: Latitude coordinate of camera (float)
    lng: longitude coordinate of camera (float)
    index: Calculated index of mask-wearing individuals (int)
@return: None
"""
def update(lat, lng, index):
    data = db.get()
    for obj in data.each():
        if lat == obj.val().get('lat') and lng == obj.val().get('lng'):
            key = obj.key()
            db.child(key).update({"avgIndex": index})

"""
Function: newCamera
Creates and initializes new camera location in Firebase DB
@param
    lat: Latitude coordinate of camera (float)
    lng: longitude coordinate of camera (float)
@return: None
"""
def newCamera(lat, lng, index):
    data = {"avgIndex": index, "lat": lat, "lng": lng}
    db.push(data)

######################### IGNORE BELOW THIS LINE #######################################



####### FUNCTION TO ADD RANDOM DISTRIBUTION OF COORDINATES/INDICES ###########
#for i in range(250):
#    newCamera(random.uniform(-90,90), random.uniform(-180,180),random.randrange(0,100,1))

# update(10, 10, 60)
# update(123.123, 123.123, 85)
# update(72.567, 90.349, 90)
# db.child("data").update({"text": "Blahblahblah"})
# update(32.7767, -96.7970, 99)

#################### MISC NOTES AND TESTING ####################
# Core Functionalities
# a) Real-time collection of datapoints from video feeds
#      CV algo spits out data every so often -> update DB -> Run averaging calculation to generate index -> Push to frontend
# b) Real-time display of data to frontend
#      Read from DB every so often -> dump data to Google Map API

# To-do:
# Do users upload own vids? Or are we just using public CCTV?
# Is Flask/web framework necessary?  User interaction seems to be solely interacting with map
#   Set up pipeline btwn CV algo and DB (be mindful of FireBase read/write limits)
#   Frontend datadump set on timer?
# from flask import Flask, render_template, request

