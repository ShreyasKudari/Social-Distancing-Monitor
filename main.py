# # Core Functionalities
# # a) Real-time collection of datapoints from video feeds
# #      CV algo spits out data every so often -> update DB -> Run averaging calculation to generate index -> Push to frontend
# # b) Real-time display of data to frontend
# #      Read from DB every so often -> dump data to Google Map API

# # To-do:
# # Do users upload own vids? Or are we just using public CCTV?
# # Is Flask/web framework necessary?  User interaction seems to be solely interacting with map
# #   Set up pipeline btwn CV algo and DB (be mindful of FireBase read/write limits)
# #   Frontend datadump set on timer?

# from flask import Flask, render_template, request, jsonify
# import requests
# # import pyrebase

# # Basic FireBase Connection
# config = {
#     "apiKey": "AIzaSyAf58ybK5T7_dZr10b4tum-XAu3aqu1v_Q",
#     "authDomain": "social-distancing-monito-c9b2c.firebaseapp.com",
#     "databaseURL": "https://social-distancing-monito-c9b2c.firebaseio.com",
#     "projectId": "social-distancing-monito-c9b2c",
#     "storageBucket": "social-distancing-monito-c9b2c.appspot.com",
#     "messagingSenderId": "847811129335",
#     "appId": "1:847811129335:web:505c7263ef941efeaf88f2",
#     "measurementId": "G-H2DKQT2CK8"
# }

# firebase = pyrebase.initialize_app(config)
# db = firebase.database()

# db.child("names").remove()

# # Basic Flask Template

# # run "set FLASK_APP=main.py" and then "flask run"

# app = Flask(__name__)

# example_data = {
#     'loc1': [
#         {
#             'name':'dallas',
#             'coords':'12345'
#         }
#     ]
# }

# data_json = json.dumps(example_data)

# @app.route('/hello', methods=['POST', 'GET'])
# def index():

#     # POST request
#     if request.method == 'POST':
#         print('Incoming...')
#         print(request.get_json())
#         return 'OK'

#     # GET request    
#     else:
#         message = {'greeting': 'Hello from Flask!'}
#         return jsonify(message)

    
# # @app.route('/test')
# # def test_page():
# #     return render_template('index.html')

# if __name__ == "__main__":
#     app.run(debug=True)
