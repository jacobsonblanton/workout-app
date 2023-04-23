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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='client_user')

class Coach(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # establishing the relationship between the user and coach tables
    # this allows us to access the user attributes from the coach table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='user')
    
class Weight(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    new_weight = db.Column(db.Float,)
    date_created = db.Column(db.Date, default=datetime.now())
        
