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

@app.route('/variants', methods=['GET'])
def getAllVariants():
    # body = request.json
    # email = body['email']

    variants = Variants.query.all()
    
    # users = User.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    for variant in variants:
        id = variant.id
        variantValue = VariantValues.query\
        .filter_by(variants_id = id)\
        .all()
        print(variantValue)
        variantValList = []
        if variantValue:
            for val in variantValue:
                variantValList.append(val.value)
                # variantValList.append({
                # 'id':val.id,
                # 'value' : val.value
                # })
        print(variantValList)
        # for val in variantValue:
        #     variantValList.append(val)
        # variantValue = VariantValues.query.all(id)
        # variantValue = VariantValues.query.all()
        output.append({
            'id':variant.id,
            'name' : variant.name,
            'varinatValue': variantValList
        })

    return jsonify({'variant': output})   

@app.route('/variants', methods=['POST'])
def postVariant():
    body = request.json
    print(body)
    name = body['name']
    product_id = body['product_id']
    

    varnt = Variants.query\
        .filter_by(name = name)\
        .first()
    if not varnt:
        variants = Variants(
            name = name,
            product_id = product_id
        )
        db.session.add(variants)
        db.session.commit()

        return make_response('Successfully Created.', 201)
    else:
        # returns 202 if user already exists
        return make_response('Error in variant creation.', 202)

