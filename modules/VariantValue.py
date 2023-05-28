from flask import Flask, render_template, request, jsonify, make_response, session,redirect,url_for
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import yaml
from config import  User, Product, Category,Plan,PlanFeature,Variants, VariantValues
from config import db, app,mail
from uuid import uuid4 # for public id
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
import modules.Login
import modules.Category
import modules.Plan

@app.route('/variantvalue', methods=['GET'])
def getAllVariantValue():
    # body = request.json
    # email = body['email']

    variantsvalue = VariantValues.query.all()
    
    # users = User.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    for variantvalue in variantsvalue:
        variant = Variants.query\
        .filter_by(id = variantvalue.variants_id)\
        .first()

        output.append({
            'id':variantvalue.id,
            'value' : variantvalue.value,
             'name': variant.name
        })

    return jsonify({'variantvalue': output})   

@app.route('/variantvalue', methods=['POST'])
def postVariantValue():
    body = request.json
    print(body)
    value = body['value']
    variants_id = body['variants_id']
    
    varntval = VariantValues.query\
        .filter_by(value = value)\
        .first()
    if not varntval:
        variantvalue = VariantValues(
            value = value,
            variants_id = variants_id
        )
        db.session.add(variantvalue)
        db.session.commit()

        return make_response('Successfully Created.', 201)
    else:
        # returns 202 if user already exists
        return make_response('Error in variant value creation.', 202)

