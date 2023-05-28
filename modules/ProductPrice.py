from flask import Flask, render_template, request, jsonify, make_response, session,redirect,url_for
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import yaml
from config import  User, Product, Category,Plan,PlanFeature,Variants, VariantValues,ProductPrices
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


@app.route('/variantvalue/<id>', methods=['GET'])
def getAllVariantValues(id):
    print(id)
    
    variantsval = VariantValues.query\
        .filter_by(variants_id = id)\
        .all()
    output = []
    for val in variantsval:
        output.append({
        'id':val.id,
        'value' : val.value,
        'variants_id': val.variants_id
        })
        print(output)

    return jsonify({'variantValue': output})   

@app.route('/logo',methods=['GET'])
def logo():
    print("logo")
    with open("product1.jpg", 'rb') as bites:
        return send_file(
            io.BytesIO(bites.read()),
            attachment_filename='logo.jpeg',
            mimetype='image/jpg'
        )
        
@app.route('/productprice', methods=['GET'])
def getAllProductPrices():
    print(id)
    productPrice = ProductPrices.query.all()
    output = []
    price = ProductPrices.query.join(Product,ProductPrices.product_id == Product.id )
    for prd in productPrice:
        # variantValList= []
        # thisdict = {
        # }
        product = Product.query\
        .filter_by(id = prd.product_id)\
        .first()
        category = Category.query\
        .filter_by(id = product.category_id)\
        .first()
        varVal = VariantValues.query\
        .filter_by(id = prd.variantValues_id)\
        .first()
        var = Variants.query\
        .filter_by(id = varVal.variants_id)\
        .first()
        # thisdict[var] = varVal

        output.append({
        'id':prd.id,
        'stockAvailable':prd.stockAvailable,
        'stockOrdered':prd.stockOrdered,
        'product': {'name' : product.name, 'id' : product.id,'description' : product.description, 'autoReduceStock' : product.autoReduceStock},
        'mrp':prd.mrp,
        'ourPrice' : prd.ourPrice,
        'image': product.image,
        'variant': {'name' : var.name, 'id' : var.id},
        'variantvalue': {'value' : varVal.value, 'id' : varVal.id},
        # 'variant': {var.name : varVal.value},
        'category':category.name
        # 'variants_id': prd.variants_id
        })
        
    print(price)
    return jsonify({'productprice': output})   

@app.route('/productprice', methods=['POST'])
def postProductPrices():
    body = request.json
    print(body)
    # rand_token = uuid4()
    sKUNo = str(random.randint(100000, 999999))
    taxPercent  = body['taxPercent']
    taxonMRP = body['taxonMRP']
    mrp = body['mrp']
    discountPercent = body['discountPercent']
    shippingCharge = body['shippingCharge']
    ourPrice = body['ourPrice']
    stockAvailable = body['stockAvailable']
    stockOrdered = body['stockOrdered']
    product_id = body['product_id']
    # variants_id = body['variants_id']
    variantValues_id = body['variantValues_id']
    
    prd = ProductPrices.query\
        .filter_by(variantValues_id = variantValues_id)\
        .first()
    
    if not prd:
        productprices = ProductPrices(
            sKUNo = sKUNo,
            taxPercent = taxPercent,
            taxonMRP = taxonMRP,
            mrp = mrp,
            discountPercent = discountPercent,
            shippingCharge = shippingCharge,
            ourPrice = ourPrice,
            stockAvailable = stockAvailable,
            stockOrdered = stockOrdered,
            product_id = product_id,
            variantValues_id = variantValues_id
        )
        db.session.add(productprices)
        db.session.commit()

        return make_response('Successfully Created.', 201)
    else:
        return make_response('SKU No is already exist', 202)


@app.route('/productprice/<id>', methods=['PUT'])
def putProductPrice(id):
    body = request.json
    id = body['id']
    productPrice = ProductPrices.query.get(id)
    if productPrice:
        # productPrice.taxPercent = body['taxPercent']
        # productPrice.taxonMRP = body['taxonMRP']
        productPrice.mrp = body['mrp']
        # productPrice.discountPercent = body['discountPercent']
        # productPrice.shippingCharge = body['shippingCharge']
        productPrice.ourPrice = body['ourPrice']
        productPrice.stockAvailable = body['stockAvailable']
        productPrice.stockOrdered = body['stockOrdered']
        productPrice.variantValues_id = body['variantValues_id']
        db.session.commit()
        return make_response('Product Price updated.', 200)
    else:
        # returns 202 if user already exists
        return make_response('Product Price not modified.', 202)


@app.route('/productprice/<id>', methods =['DELETE'])
def deleteProductPrice(id):
    # creates a dictionary of the form data
    productPrices = ProductPrices.query.get(id)
    
    print(productPrices)
    if productPrices:
        if productPrices:
            db.session.delete(productPrices)
            db.session.commit()
            return make_response('Product Price Deleted.', 200)
    else:
        # returns 202 if user already exists
        return make_response('Error in Product Price Deletion.', 202)       