from flask import Flask, render_template, request, jsonify, make_response, session,redirect,url_for,send_file
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import yaml
from config import  User, Product, Category,Plan,PlanFeature
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
import base64

#------------------------Product API Start----------------------

@app.route('/products', methods=['GET'])
def getAllProducts():
    # body = request.json
    # email = body['email']

    products = Product.query.all()
    
    # users = User.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    if products:
        print(products)
        for product in products:
            # appending the user data json
            # to the response list
            # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
            output.append({
                'id':product.id,
                'name' : product.name,
                'autoReduceStock' : product.autoReduceStock,
                'freeItem' : product.freeItem,
                'createdDate' : (product.createdDate).strftime("%Y-%m-%d"),
                'updatedDate' : (product.updatedDate).strftime("%Y-%m-%d"),
                # 'skuNo' : product.skuNo,
                'description' : product.description,
                'image' : product.image,
                'category_id':product.category_id,
                # 'full_filename': full_filename
            })
            # imageresponse = getImagePath(product.image)

        return jsonify({'products': output})
    else:
        return jsonify({'message': 'products not available'})

import io
from flask import Flask, send_file

app = Flask(__name__)

@app.route('/image/<id>', methods=['GET'])
def getImagePath(id):
    imageName = "Product-847498.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'],imageName)
    print(filepath)
    print(filepath.replace("./", ""))
    
    response = make_response(send_file(filepath.replace("./", ""),mimetype='image/png'))
    # response.headers['Content-Transfer-Encoding']='base64'
    return response

@app.route('/products/<id>', methods=['GET'])
def getProduct(id):
    # args = request.args
    # prd = Product.query.get(id)
    product = Product.query\
        .filter_by(id = id)\
        .first()
    print(product.name)
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
    obj = {
            'id':product.id,
            'name' : product.name,
            'autoReduceStock' : product.autoReduceStock,
            'freeItem' : product.freeItem,
            'createdDate' : product.createdDate,
            'updatedDate' : product.updatedDate,
            # 'skuNo' : product.skuNo,
            'description' : product.description,
            'category_id':product.category_id,
            'image' : product.image,
            'full_filename': full_filename
    }

    return jsonify({'product': obj})


@app.route('/products', methods=['POST'])
def postProduct():
    body = request.form
    print(body)
    rand_token = uuid4()
    name = body['name']
    # autoReduceStock = body['autoReduceStock']
    autoReduceStock : bool  = bool(request.form.get('autoReduceStock', False))
    freeItem : bool = bool(request.form.get('freeItem', False))
    createdDate = body['createdDate']
    updatedDate = body['updatedDate']
    # skuNo = body['skuNo']
    description = body['description']
    category_id = body['category_id']
    

    prd = Product.query\
        .filter_by(name = name)\
        .first()
    if not prd:
        uploadfile = request.files['file']
        fileName = uploadfile.filename
        imageName = fileName.split(".")
        image = "Product-"+str(random.randint(100000, 999999))+"."+imageName[1]
        path = os.path.join(app.config['UPLOAD_FOLDER'], image)
        uploadfile.save(path)
        # database ORM object
        product = Product(
            name = name,
            autoReduceStock = autoReduceStock,
            freeItem = freeItem,
            createdDate = createdDate,
            updatedDate = updatedDate,
            # skuNo = str(random.randint(100000, 999999)),
            description = description,
            category_id = category_id,
            image = image
        )
        db.session.add(product)
        db.session.commit()

        return make_response('Successfully Created.', 201)
    else:
        # returns 202 if user already exists
        return make_response('Error in product creation.', 202)

@app.route('/products', methods=['PUT'])
def putProduct():
    body = request.json
    id = body['id']
    product = Product.query.get(id)
    if product:
        product.name = body['name']
        product.autoReduceStock : bool  = bool(request.form.get('autoReduceStock', False))
        product.freeItem : bool = bool(request.form.get('freeItem', False))
        # product.autoReduceStock = body['autoReduceStock']
        # product.freeItem = body['freeItem']
        product.createdDate = body['createdDate']
        product.updatedDate = body['updatedDate']
        # product.skuNo = body['skuNo']
        product.image = body['image']
        product.description = body['description']
        product.category_id = body['category_id']
        # db.session.update(product)
        db.session.commit()
        # return jsonify({'category': category})
        return make_response('Product updated.', 200)
    else:
        # returns 202 if user already exists
        return make_response('Product not modified.', 202)


@app.route('/products/<id>', methods =['DELETE'])
def deleteProduct(id):
    product = Product.query.get(id)
    print(product)
    if product:
        db.session.delete(product)
        db.session.commit()
        return make_response('Product Deleted.', 200)
    else:
        # returns 202 if user already exists
        return make_response('Error in Product Deletion.', 202)

#------------------------Product API End----------------------

#------------------------Varient API Start----------------------

