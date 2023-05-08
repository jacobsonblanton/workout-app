# importing the necessary modules 
from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import UserMixin, login_manager, login_user, login_required, logout_user, current_user, LoginManager
from sqlalchemy import DATETIME
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy.sql import func

# creating a User class and object. Declaring what will be stored under User in the database.
# creating User relationships
# Relationships with the User and other class objects are defined as one-to-many relationship with (the User can have many workouts, User can have many ..., etc)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    starting_weight = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    cals = db.Column(db.Integer, nullable=True)
    job_type = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(200), nullable=True)
    workout_days = db.Column(db.String(200), nullable=True)
    training_focus = db.Column(db.String(200), nullable=True)
    client = db.relationship('Client', backref='client')
    coach = db.relationship('Coach', backref='coach')
    weight = db.relationship('Weight', backref='weight')
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # establishing the relationship between the user and client tables
    # this allows us to access the user attributes from the client table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='client_user')

class Coach_Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', backref='client_coach')
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'), nullable=False)
    coach = db.relationship('Coach', backref='coach_client')

class Coach(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # establishing the relationship between the user and coach tables
    # this allows us to access the user attributes from the coach table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='user')
    
class Weight(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    new_weight = db.Column(db.Integer,)
    date_created = db.Column(db.Date, default=datetime.now())

# six day workout split (ULULUL)
class Upper_One(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_upper_1')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Lower_One(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_lower_1')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Upper_Two(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_upper_2')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Lower_Two(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_lower_2')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Upper_Three(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_upper_3')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Lower_Three(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_lower_3')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

# five day workout split (ULPPL)
class UL_PPL_One(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_ul_ppl_1')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class UL_PPL_Two(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_ul_ppl_2')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class UL_PPL_Three(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_ul_ppl_3')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class UL_PPL_Four(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_ul_ppl_4')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class UL_PPL_Five(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_ul_ppl_5')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

# four day workout split (full body 1 2 3 4)
class Full_Body_One_4day(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_full_body_1_4')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    exercise8 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Full_Body_Two_4day(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_full_body_2_4')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Full_Body_Three_4day(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_full_body_3_4')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Full_Body_Four_4day(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_full_body_4_4')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

# three day workout split (full body 1 2 3)
class Full_Body_One(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_full_body_1')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    exercise8 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Full_Body_Two(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_full_body_2')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    exercise8 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Full_Body_Three(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_full_body_3')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    exercise8 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

# two day workout split (UL)
class Upper_2day(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_upper_2day')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    exercise8 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Lower_2day(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    user = db.relationship('User', backref='user_lower_2day')
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())