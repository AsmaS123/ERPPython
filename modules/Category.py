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


@app.route('/category', methods =['POST'])
def category():
    # creates a dictionary of the form data
    body = request.json
    print(body)
    name = body['name']
    active = body['active']
    print(name)
    category = Category.query\
        .filter_by(name = name)\
        .first()
    print(category)
    if not category:
        # database ORM object
        category = Category(           
            name = name,
            active = active,
            # noOfSubCategory = 0
        )
        # insert user
        print(category, "user value")
        db.session.add(category)
        db.session.commit()

        return make_response('Category Created.', 201)
    else:
        # returns 202 if user already exists
        return make_response('Category Name already exists.', 202)

@app.route('/category/<id>', methods =['PUT'])
def putcategory(id):
    # creates a dictionary of the form data
    category = Category.query.get(id)

    print(category)
    if category:
        product = Product.query.filter_by(category_id = category.id).all()
        # print(product)
        if product:
            return make_response('Category not Updated.', 200)
        else:
            body = request.json
            print(body)
            name = body['name']
            active = body['active']

            category.name = name
            category.active = active

            db.session.commit()
            return make_response('Category updated.', 200)
    else:
        # returns 202 if user already exists
        return make_response('Category Name already exists.', 202)

@app.route('/category/<id>', methods =['DELETE'])
def deletecategory(id):
    # creates a dictionary of the form data
    category = Category.query.get(id)
    
    print(category)
    if category:
        product = Product.query.filter_by(category_id = category.id).all()
        print(product)
        if product:
            return make_response('Category not Deleted.', 200)
        else:
            db.session.delete(category)
            db.session.commit()
            return make_response('Category Deleted.', 200)
    else:
        # returns 202 if user already exists
        return make_response('Category Name already exists.', 202)

@app.route('/categories', methods=['GET'])
def get_all_category_details():
    categories = Category.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    subcat = []
    for category in categories:
        output.append({
            'id' : category.id,
            'name' : category.name,
            'active' : category.active
        })
    return jsonify({'category': output})
    



    
#SubCategory not required
@app.route('/subcategory', methods =['POST'])
def subcategory():
    # creates a dictionary of the form data
    body = request.json
    # print(body)
    name = body['name']
    active = body['active']
    category_id = body['category_id']
    # print(category_id)
    subcategory = SubCategory.query\
        .filter_by(name = name)\
        .first()
    category = Category.query\
        .filter_by(id = category_id)\
        .first()
    # print(category)
    # print(category)
    if not subcategory:
        # database ORM object
        scategory = SubCategory(           
            name = name,
            active = active,
            noOfProduct = 0,
            category_id = category_id
        )
        # print(scategory)
        db.session.add(scategory)
        db.session.commit()
        # insert user
        # print(scategory, "user value")
    if category:
        redirect(url_for('putcategory',id = category_id,methods =['PUT']))
        # print(noOfSubCategory, category.noOfSubCategory+1)   

        return make_response('subcategory Created.', 201)
    else:
        # returns 202 if user already exists
        return make_response('subcategory Name already exists.', 202)



# @app.route('/category', methods=['GET'])
# def get_all_category():
#     categories = Category.query.all()
#     # converting the query objects
#     # to list of jsons
#     output = []
#     for category in categories:
#         # appending the user data json
#         # to the response list
#         output.append({
#             'id' : category.id,
#             'name' : category.name,
#             # 'active' : category.active
#         })

#     return jsonify({'category': output})