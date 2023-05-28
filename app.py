from flask import Flask, render_template, request, jsonify, make_response, session,redirect,url_for
# from flask_sqlalchemy import SQLAlchemy
# import yaml
# from config import  User, Product, Category,Plan,PlanFeature,UserAddress
# from config import db, app,mail
import uuid # for public id
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
# import pyotp
import vonage
import smtplib
# from flask_mail import Mail
import math
# import random
from flask_session import Session
import random
# from flask_mail import *
from flask_mail import Mail, Message

# from config import mail
import os
from config import app
import requests
from flask_cors import CORS, cross_origin
from flask_session import Session

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#import modules
import modules.Login
import modules.Category
import modules.Plan
import modules.Product
import modules.Variant
import modules.VariantValue
import modules.ProductPrice
import modules.Cart

CORS(app)
@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.debug = True
    app.run()


