from flask import Flask, render_template, request, jsonify, make_response, session,redirect,url_for
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import yaml
from config import  User, Product,UserAddress ,Category,Plan,PlanFeature,Cart
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


@app.route('/cart', methods =['POST'])
def cart():
    # creates a dictionary of the form data
    body = request.json
    print(body)
    date = "2023-04-19 12:13:42.518"
    isActive : bool  = bool(body.get('isActive', False))
    grossAmount = body['grossAmount']
    taxAmount = body['taxAmount']
    shippingCharge = body['shippingCharge']
    netAmount = body['netAmount']
    amountPayable = body['amountPayable']
    product_id = body['product_id']
    users_public_id = body['users_public_id']

    cart = Cart(           
        cartNo = str(random.randint(100000, 999999)),
        date = date,
        grossAmount = grossAmount,
        taxAmount = taxAmount,
        shippingCharge = shippingCharge,
        netAmount = netAmount,
        amountPayable = amountPayable,
        isActive = isActive,
        product_id = product_id,
        users_public_id = users_public_id
    )
    # insert user
    print(cart, "user value")
    db.session.add(cart)
    db.session.commit()

    return make_response('Cart Created.', 201)
    # else:
    #     # returns 202 if user already exists
    #     return make_response('Category Name already exists.', 202)


@app.route('/cart', methods=['GET'])
def get_all_cart_details():
    cart = Cart.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    for crt in cart:
        output.append({
            'id' : crt.id,
            'cartNo' : crt.cartNo,
            'grossAmount' : (crt.grossAmount).__str__(),
            'taxAmount' : crt.taxAmount,
            'shippingCharge' : crt.shippingCharge,
            'netAmount' : (crt.netAmount).__str__(),
            'amountPayable' : crt.amountPayable,
            'isActive' : crt.isActive,
            'product_id' : crt.product_id,
            'users_public_id' : crt.users_public_id
        })
    return jsonify({'cart': output})