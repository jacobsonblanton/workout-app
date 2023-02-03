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
    upper_one = db.relationship('Upper_One', backref='user')
    lower_one = db.relationship('Lower_One', backref='user')
    upper_two = db.relationship('Upper_Two', backref='user')
    lower_two = db.relationship('Lower_Two', backref='user')
    upper_three = db.relationship('Upper_Three', backref='user')
    lower_three = db.relationship('Lower_Three', backref='user')
    full_body_one = db.relationship('Full_Body_One', backref='user')
    full_body_two = db.relationship('Full_Body_Two', backref='user')
    full_body_three = db.relationship('Full_Body_Three', backref='user')
    full_body_one_4day = db.relationship('Full_Body_One_4day', backref='user')
    full_body_two_4day = db.relationship('Full_Body_Two_4day', backref='user')
    full_body_three_4day = db.relationship('Full_Body_Three_4day', backref='user')
    full_body_four_4day = db.relationship('Full_Body_Four_4day', backref='user')
    ul_ppl_one = db.relationship('UL_PPL_One', backref='user')
    ul_ppl_two = db.relationship('UL_PPL_Two', backref='user')
    ul_ppl_three = db.relationship('UL_PPL_Three', backref='user')
    ul_ppl_four = db.relationship('UL_PPL_Four', backref='user')
    ul_ppl_five = db.relationship('UL_PPL_Five', backref='user')
    new_weight = db.relationship('Weight', backref='user')
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Upper_One(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Lower_One(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Upper_Two(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Lower_Two(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Upper_Three(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Lower_Three(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Full_Body_One(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    exercise8 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Full_Body_One_4day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Full_Body_Three_4day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Full_Body_Four_4day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class UL_PPL_One(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class UL_PPL_Two(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class UL_PPL_Three(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class UL_PPL_Four(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    exercise7 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class UL_PPL_Five(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())


class Upper_2day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise1 = db.Column(db.String(200), nullable=True)
    exercise2 = db.Column(db.String(200), nullable=True)
    exercise3 = db.Column(db.String(200), nullable=True)
    exercise4 = db.Column(db.String(200), nullable=True)
    exercise5 = db.Column(db.String(200), nullable=True)
    exercise6 = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    new_weight = db.Column(db.Integer, nullable= True)
    date_created = db.Column(db.Date, default=datetime.now())

    

        
