from flask import Flask, render_template, request, jsonify,session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from model import db,User
# import yaml
import vonage
import smtplib
from flask_mail import Mail
from flask_session import Session
from datetime import datetime
from flask import *
from flask_mail import *
from random import *
from flask_migrate import Migrate

app = Flask(__name__)
mail = Mail(app)
app.config['SECRET_KEY'] = 'your secret key'
# db_config = yaml.load(open('database.yaml'))
# app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri'] 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Passme@localhost:5432/ERP-database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'asmanoushin.786@gmail.com'
app.config['MAIL_PASSWORD'] = 'Passme@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000,999999)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# mail = Mail(app)
import os
Image_FOLDER = os.path.join('asset', 'image')
app.config['UPLOAD_FOLDER'] = Image_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique = True)
    sponcer_id = db.Column(db.String(50), unique = True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    contactNo = db.Column(db.String(80))
    nominee = db.Column(db.String(100))
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    userAdd = db.relationship("UserAddress", uselist=False,back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.firstName

class UserAddress(db.Model):
    __tablename__ = "useraddress"
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(80))
    state = db.Column(db.String(100))
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    pinCode = db.Column(db.Integer)
    contactNo = db.Column(db.String(80))
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="userAdd")
    # users = db.relationship('User')
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<UserAddress %r>' % self.contactNo

class ReferalUser(db.Model):
    __tablename__ = "referalusers"
    id = db.Column(db.Integer, primary_key=True)
    user_sponcer_id = db.Column(db.String(50), db.ForeignKey('users.sponcer_id'))
    email = db.Column(db.String(120), unique=True)
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<ReferalUser %r>' % self.email

class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique = True)
    image = db.Column(db.String(120))
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    gender = db.Column(db.String(120), unique=True)
    contactNo = db.Column(db.String(80))
    country = db.Column(db.String(80))
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    city = db.Column(db.String(100))
    pinCode = db.Column(db.Integer)
    address = db.Column(db.String(100))
    education = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    payBand = db.Column(db.String(100))
    registerNo = db.Column(db.String(100))
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Employee %r>' % self.name

class PlanFeature(db.Model):
    __tablename__ = "planfeature"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<PlanFeature %r>' % self.name

class Plan(db.Model):
    __tablename__ = "plan"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    planfeatures = db.relationship(
        "PlanFeature",
        backref="plan",
        cascade="all, delete, delete-orphan",
        single_parent=True,
    )
    def __repr__(self):
        return '<Plan %r>' % self.name



# inventory start

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Category %r>' % self.name

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description  = db.Column(db.String(100))
    autoReduceStock = db.Column(db.Boolean, default=False)
    freeItem = db.Column(db.Boolean, default=False)
    createdDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedDate = db.Column(db.DateTime, nullable=False)
    # skuNo = db.Column(db.String(100),unique = True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')
    image = db.Column(db.String(100),unique = True)

    prdprice = db.relationship("ProductPrices", back_populates="product")
    variant = db.relationship("Variants", back_populates="product")
    # variantval = db.relationship("VariantValues", back_populates="product")

    def __repr__(self):
        return '<Product %r>' % self.name

class Variants(db.Model):
    __tablename__ = "variants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product',back_populates="variant")

    def __repr__(self):
        return '<Variants %r>' % self.name

class VariantValues(db.Model):
    __tablename__ = "variantValues"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100))
    variants_id = db.Column(db.Integer, db.ForeignKey('variants.id'))
    # product = db.relationship('Product',back_populates="variantval")

    def __repr__(self):
        return '<VariantValues %r>' % self.value


class ProductPrices(db.Model):
    __tablename__ = "productPrices"
    id = db.Column(db.Integer, primary_key=True)
    sKUNo =  db.Column(db.Integer)
    taxPercent = db.Column(db.Float)
    taxonMRP = db.Column(db.Float)
    mrp = db.Column(db.Integer)
    discountPercent = db.Column(db.Float)
    shippingCharge = db.Column(db.Float)
    ourPrice = db.Column(db.Float)
    stockAvailable = db.Column(db.Boolean, default=False)
    stockOrdered = db.Column(db.Boolean, default=False)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product',back_populates="prdprice")
    #  variantCombinations_id = db.Column(db.Integer, db.ForeignKey('variantCombinations.id'))
    variantValues_id = db.Column(db.Integer, db.ForeignKey('variantValues.id'))
    
    def __repr__(self):
        return '<ProductPrices %r>' % self.sKUNo

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    orderNo =  db.Column(db.Integer)
    mobileNo =  db.Column(db.Integer)
    postalCode = db.Column(db.String(100))
    area = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    doorNo = db.Column(db.String(100))
    
    totalItems = db.Column(db.Integer)
    totalAmount = db.Column(db.Float)
    totalMRP = db.Column(db.Float)
    totalTax = db.Column(db.Float)
    additionalShippingCharges = db.Column(db.Float)
    totalDiscount = db.Column(db.Float)
    couponDiscount = db.Column(db.Float)
    netAmount = db.Column(db.Float)
    status = db.Column(db.Boolean, default=False)
    paymentType =  db.Column(db.Integer)
    paymentStatus =  db.Column(db.Integer)
    paymentDate = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.String(100))
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('User')

    def __repr__(self):
        return '<Order %r>' % self.orderNo


class OrderDetails(db.Model):
    __tablename__ = "orderDetails"
    id = db.Column(db.Integer, primary_key=True)
    sKUNo =  db.Column(db.Integer)
    offerCode = db.Column(db.String(100))
    mrp = db.Column(db.Float)
    ourPrice = db.Column(db.Float)
    quantity =  db.Column(db.Integer)
    quantityPacked =  db.Column(db.Integer)
    quantityToPacked =  db.Column(db.Integer)
    amount = db.Column(db.Float)
    discount = db.Column(db.Float)
    discountType = db.Column(db.Integer)
    discountAmount = db.Column(db.Float)
    taxPercent = db.Column(db.Integer)
    taxAmount = db.Column(db.Float)
    shippingCharge = db.Column(db.Float)
    lineAmount = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order')

    def __repr__(self):
        return '<OrderDetails %r>' % self.sKUNo

class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    cartNo =  db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False)
    grossAmount = db.Column(db.Float)
    taxAmount = db.Column(db.Float)
    shippingCharge = db.Column(db.Float)
    netAmount = db.Column(db.Float)
    amountPayable = db.Column(db.Float)
    isActive = db.Column(db.Boolean, default=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    users_public_id = db.Column(db.String, db.ForeignKey('users.public_id'))

    product = db.relationship('Product')
    users = db.relationship('User')

    def __repr__(self):
        return '<Cart %r>' % self.cartNo

class WishLists(db.Model):
    __tablename__ = "wishLists"
    id = db.Column(db.Integer, primary_key=True)
    autoProcess = db.Column(db.Boolean, default=False)
    autoProcessDate = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product')

    def __repr__(self):
        return '<WishLists %r>' % self.autoProcess

class WishListDetails(db.Model):
    __tablename__ = "wishListDetails"
    id = db.Column(db.Integer, primary_key=True)
    sKUNo =  db.Column(db.Integer)
    offerCode = db.Column(db.String(100))
    quantity =  db.Column(db.Integer)

    def __repr__(self):
        return '<WishListDetails %r>' % self.sKUNo

class PaymentDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    provider = db.Column(db.Float)
    isActive = db.Column(db.Boolean, default=False)
    createdDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedDate = db.Column(db.DateTime, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    # order = db.relationship('Order')
    
app.app_context().push()
db.create_all()
db.session.commit()
