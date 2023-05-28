from flask import Flask, render_template, request, jsonify,session,url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from sqlalchemy.sql import func
# from model import db,User
# import yaml
import vonage
import smtplib
from flask_mail import Mail
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
# db_config = yaml.load(open('database.yaml'))
# app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri'] 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Passme@localhost:5432/flask_new'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'c727d9dba300c5'
app.config['MAIL_PASSWORD'] = '7a78da8a956ba9'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
mail = Mail(app)

db = SQLAlchemy(app)
CORS(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'

db.create_all()
# db.session.commit()