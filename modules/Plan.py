from flask import Flask, render_template, request, jsonify, make_response, session,redirect,url_for
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import yaml
from config import  User, Product, Category,Plan,PlanFeature
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

@app.route('/plan', methods=['GET'])
def get_all_plans():
    plans = Plan.query.all()
    features = PlanFeature.query.all()
    # print(features)
    output = []
    outputf = []
    for plan in plans:
        for feature in features:
            if feature.plan_id == plan.id:
                outputf.append(feature.name)        
        output.append({
            'id' : plan.id,
            'name' : plan.name,
            'price': plan.price,
            'dateTime':plan.dateTime,
            'feature': outputf
            # 'active' : category.active
        })
        outputf = []
    return jsonify({'plan': output})

@app.route('/plan', methods =['POST'])
def post_plan():
    # creates a dictionary of the form data
    body = request.json
    name = body['name']
    price = body['price']
    dateTime = body['dateTime']
    features = body['featureList']
    # print(features)
    # database ORM object
    plan = Plan(
        name = name,
        price = price,
        dateTime = dateTime,
    )
    for featureName in features:
        # print(featureName)
        plan.planfeatures.append(PlanFeature(name = featureName, dateTime = dateTime))

    # insert user
    print(plan, "plan value")
    db.session.add(plan)
    db.session.commit()

    return make_response('Successfully registered.', 201)

@app.route('/plan', methods =['PUT'])
def put_plan():
    # creates a dictionary of the form data
    body = request.json
    id = body['id']
    name = body['name']
    price = body['price']
    dateTime = body['dateTime']
    features = body['featureList']
    # print(body)
    # database ORM object
    plan = Plan.query.get(id)
    if plan:
        plan.name = name
        plan.price = price
        plan.dateTime = dateTime

        feature = PlanFeature.query.filter(PlanFeature.plan_id == id).all()
        print(feature)
        # for featureName in features:
        #     plan.planfeatures.append(PlanFeature(name = featureName, dateTime = dateTime))

        db.session.commit()

        return make_response('Successfully updated plan.', 200)
    else:
        return make_response('Plan not modified.', 202)
