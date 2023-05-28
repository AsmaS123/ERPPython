from flask import Flask, render_template, request, jsonify, make_response, session,redirect,url_for
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import yaml
from config import  User, Product,UserAddress ,Category,Plan,PlanFeature
from config import db, app,mail
import uuid # for public id
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
import pyotp
import vonage
import smtplib
# from flask_mail import Mail
import math
# import random
from flask_session import Session
import random
# from flask_mail import *
from flask_mail import Mail, Message

from config import mail
import os
from config import app
import requests


UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        token = request.headers['x-access-token']
        # print(token)
        if 'x-access-token' in request.headers:
            print(token)
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            # data = app.config['SECRET_KEY']
            data = jwt.decode(token,app.config['SECRET_KEY'], algorithms=["HS256"])
            print(data['id'])
            current_user = User.query\
                .filter_by(id = data['id'])\
                .first()
            print(current_user)
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)
    return decorated

# User Database Route
# this route sends back list of users users

@app.route('/user/<id>', methods = ['GET'])
@token_required
def get_users(id):
    print(id)
    if id:
        user = User.query.get(id)
        print(user)
        if user:
            obj = {
            'id':user.id,
            'email' : user.email,
            'firstName' : user.firstName,
            'lastName' : user.lastName,
            'password':user.password,
            'contactNo':user.contactNo,
            'nominee':user.nominee,
            'country':user.country,
            'state':user.state,
            'district':user.district,
            'city':user.city,
            'pinCode':user.pinCode,
            # 'policy':user.policy,
            'sponcer_id' : user.sponcer_id,
            }
            return jsonify({'users': obj})
        else:
            return "id is not exist"
    else:
        return "400 Bad request"

@app.route('/user', methods =['GET'])
def get_all_users():
    # querying the database
    # for all the entries in it
    users = User.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    for user in users:
        # appending the user data json
        # to the response list
        output.append({
            'id':user.id,
            'sponcer_id': user.sponcer_id,
            'public_id':user.public_id,
            'firstName' : user.firstName,
            'lastName':user.lastName,
            'email' : user.email,
            'password':user.password,
            'contactNo':user.contactNo,
            'nominee':user.nominee,
            # 'country':user.country,
            # 'state':user.state,
            # 'district':user.district,
            # 'city':user.city,
            # 'pinCode':user.pinCode,
            # 'policy':user.policy,
        })

    return jsonify({'users': output})

@app.route('/user/<id>', methods =['PUT'])
def putuser(id):
    # creates a dictionary of the form data
    user = User.query.get(id)
    if id:
        if user:
            body = request.json
            print(body)
            firstName = body['firstName']
            lastName = body['lastName']
            contactNo = body['contactNo']
            nominee = body['nominee']
            country = body['country']
            state = body['state']
            district = body['district']
            city = body['city']
            pinCode = body['pinCode']

            user.firstName = firstName
            user.lastName = lastName
            user.contactNo = contactNo
            user.nominee = nominee
            user.country = country
            user.state = state
            user.district = district
            user.city = city
            user.pinCode = pinCode

            db.session.commit()
            return make_response('User Updated Successfully.', 200)
        else:
            return make_response('Error in User Updating.', 202)
    else:
        return "400 Bad request"

@app.route('/user/<id>', methods =['DELETE'])
def deleteuser(id):
    print(id)
    # sponcer_id = id
    if id:
        user = User.query\
        .filter_by(id =  id)\
        .first();
        if user:
            print(user)
            db.session.delete(user)
            db.session.commit()
            return make_response('User Deleted.', 200)
        else:
            # returns 202 if user already exists
            return make_response('Error in User Deletion.', 202)
    else:
        return "400 Bad request"


@app.route('/referalLink', methods =['GET'])
def referalLink():
    url = "https://send.api.mailtrap.io/api/send"
    payload = "{\"from\":{\"email\":\"asmanoushin.786@gmail.com\",\"name\":\"Mailtrap Test\"},\"to\":[{\"email\":\"Asma.Shaikh@exelaonline.com\"}],\"subject\":\"You are awesome!\",\"text\":\"Congrats for sending test email with Mailtrap!\",\"category\":\"Integration Test\"}"
    headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJkYXRhIjp7InRva2VuIjoiMGJiMWQzOTAwODI3YTNkYTI3NDJhOTQ5ODMwOGZjMmEifX0.ADLUHs1FHTdZ-FYlHWwHhMZHLDkJnk6cWnozlylqxETCOU5lJu18ufvUhUIJgK5NwBrtuF-Ivl4H16z7vc8SBA",
    "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    # msg = Message('Hello', sender = 'asmanoushin.786@gmail.com', recipients = ['Asma.Shaikh@exelaonline.com'])
    # msg.body = "Hello Flask message sent from Flask-Mail"
    # mail.send(msg)
    # return "Sent"
    return response.text
# route for logging user in

@app.route('/login', methods =['POST'])
def login():
    # creates dictionary of form data
    body = request.json
    print(body)
    password = body['password']
    email = body['email']
    # print(email)
    if not body or not email or not password:
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )

    user = User.query\
        .filter_by(email =  body['email'])\
        .first()
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
    if check_password_hash(user.password, body.get('password')):
        # generates the JWT Token
        token = jwt.encode(
            {'id': user.id }, 
            app.config['SECRET_KEY'], 
            algorithm="HS256")
        # session["otp"] = pyotp.random_base32()
        session["token"] = token
        session["email"] = user.email
        session["public_id"] = user.public_id
        # print(session.get("otp"))
        return make_response(jsonify({'token' : token, 'email' : user.email,'sponcer_id':user.sponcer_id, 'public_id':user.public_id}), 201)
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )

@app.route("/logout",methods =['GET'])
def logout():
    session["email"] = None
    session["public_id"] = None
    return make_response('Successfully registered.', 201)
    
@app.route('/referalDetails', methods=['POST'])
def referalDetails():
    body = request.json
    email = body['email']

    user = User.query\
        .filter_by(email = email)\
        .first()
    print(user.email)

    userObj = {
    "sponcer_id": user.sponcer_id,
    "name":user.name,
    "contactNo":user.contactNo,
    "pinCode":user.pinCode,
    "country":user.country,
    "state":user.state,
    "district":user.district,
    "city":user.city,
    "nominee":user.nominee
    }

    return jsonify({'users': userObj})

@app.route('/varifyOTP', methods=['POST'])
def varifyOTP():
    """ A POST endpoint that sends an SMS. """
    body = request.json
    # Extract the form values:
    email = body['email']
    # password = body['password']
    msg = Message('OTP',sender = 'asmanoushin.786@gmail.com', recipients = [email])
    msg.body = '1234'
    mail.send(msg)

    # message = 'Generated OPT sent to your registerted mobile number'
    # msg = Message('Hello from the other side!', sender =   'asmanoushin.786@gmail.com', recipients = ['asmanoushin.123@rediffmail.com'])
    # msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
    # mail.send(msg)
    # return "Message sent!"
    # Send the SMS message:
    # responseData = sms.send_message(
    #     {
    #     'from': "Vonage APIs",
    #     'to': contactNo,
    #     'text': message,
    #     }
    # )
    # print(responseData)
    # if responseData["messages"][0]["status"] == "0":
    #     print("Message sent successfully.")
    # else:
    #     print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

# signup route

@app.route('/signup', methods =['POST'])
def signup():
    # creates a dictionary of the form data
    body = request.json
    print(body)
    firstName = body['firstName']
    lastName = body['lastName']
    email = body['email']
    sponcer_id = None
    # sponcer_id = str(random.randint(100000, 999999))
    password = body['password']
    contactNo = body['contactNo']
    country = body['country']
    state = body['state']
    address = body['address']
    city = body['city']
    pinCode = body['pinCode']
    nominee = body['nominee']
    dateTime = body['dateTime']

    # checking for existing user
    user = User.query\
        .filter_by(email = email)\
        .first()
    if not user:
        # database ORM object
        user = User(
            public_id = str(uuid.uuid4()),
            firstName = firstName,
            lastName = lastName,
            email = email,
            contactNo = contactNo,
            password = generate_password_hash(password,"sha256"),
            nominee = nominee,
            dateTime = dateTime,
            sponcer_id = sponcer_id,
            userAdd = UserAddress(
            contactNo = contactNo, 
            country = country,
            state = state,
            address = address,
            city = city,
            pinCode = pinCode,
            dateTime = dateTime
            )
        )
        
        # user.useraddress = UserAddress(
        #     contactNo = contactNo, 
        #     country = country,
        #     state = state,
        #     address = address,
        #     city = city,
        #     pinCode = pinCode,
        #     dateTime = dateTime
        # )
        # insert user
        print(user, "user value")
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)

