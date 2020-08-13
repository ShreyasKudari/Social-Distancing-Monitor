"""
    OpenCV to Firebase Library

    Requires: pyrebase
    @user$ "pip(3) install pyrebase"

    SUMMARY
    > Contains functions for updating Firebase data with data generated from OpenCV Data

    > Data currently stored as JSON: {"avgIndex": 0, "Location": "", "CamID": "", "lat": 0, "lng": 0, "Percentages": []}
        Note that some fields may currently be redundant and/or unecessary, need to determine use later

    Written by Austin Tsao
    August 12, 2020
"""

import pyrebase

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
        if lat == obj.val()['lat'] and lng == obj.val()['lng']:
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
def newCamera(lat, lng):
    data = {"avgIndex": 0, "Location": "", "CamID": "", "lat": lat, "lng": lng, "Percentages": []}
    db.push(data)


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

#init()
#newCamera(100, 300)
#update(-40.39492, 120.21345, 100)



'''
for obj in data.each():
    print(obj.val()['lat'])
    if -31.56391 == obj.val()['lat'] and 147.154312 == obj.val()['lng']:
        print(obj.key())
        key = obj.key()
        db.child(key).update({"avgIndex": 9000})

print(data.val())

#dataInput = {"avgIndex": 45, "Location": "Dallas", "CamID": "D31", "lat": -31.563910, "lng": 147.154312, "Percentages": [25,35,23,72,45]}
#dataInput2 = {"avgIndex": 90, "Location": "Fort Worth", "CamID": "F25", "lat": -40.39492, "lng": 120.21345, "Percentages": [80,30,43,23,44]}
#db.push(dataInput2)
#db.push(dataInput)
'''

'''
# Basic Flask Template
app = Flask(__name__)

@app.route('/')
def index():
    if request.method == 'POST':
        pass
    else:
        pass

    return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=True)
'''

