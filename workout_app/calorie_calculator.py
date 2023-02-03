# importing the necessary modules
import time
from .models import User 
from email.policy import default
from xmlrpc.client import DateTime
from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import UserMixin, login_manager, login_user, login_required, logout_user, current_user, LoginManager
from sqlalchemy import DATETIME
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy.sql import func

def main():
    # getting user some data about the user
    weight = float(input("What is your weight (kg)? "))
    height = float(input("What is your height (cm)? "))
    age = float(input("What is your age (years)? "))
    gender = input("What is your gender (male/female)? ") 

    # getting bmr equation based on user input and printing the bmr
    male_bmr = round(88.362 + (13.397 * weight) + (4.799 * height ) - (5.677 * age),2)
    female_bmr = round(447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age),2)

    # determining which equation to use based on gender of the user
    if gender == 'male':
        print("Your basal metabolic rate is", male_bmr, "kcal.")
    elif gender == 'female':
        print("Your basal metabolic rate is", female_bmr, "kcal.")
    else:
        print("gender must be male or female...")

    # asking the user a few more questions to determine how many calories to add to their bmr
    job_type = input("What type of job (sedentary, active, sedentary-active, active-sedentary) do you have? ")
    cardio = int(input("How much cardio do you do per week (minutes)? "))
    weight_training = int(input("How many weight training sessions do you have per week? "))

    # implementing a while loop for male and female so I can add calories to correct bmr value
    while gender == 'male':
        if job_type == 'sedentary':
            male_bmr += 300
            print("...calculating your new bmr")
            time.sleep(2)
            print("Your new bmr is", round(male_bmr,2), "kcal.")
            break
        elif job_type == 'sedentary-active':
            male_bmr += 500
            print("...calculating your new bmr")
            time.sleep(2)
            print("Your new bmr is", round(male_bmr,2), "kcal.")
            break
        elif job_type == 'active-sedentary':
            male_bmr += 700
            print("...calculating your new bmr")
            time.sleep(2)
            print("Your new bmr is", round(male_bmr,2), "kcal.")
            break
        elif job_type == 'active':
            male_bmr += 900
            print("...calculating your new bmr")
            time.sleep(2)
            print("Your new bmr is", round(male_bmr,2), "kcal.")
            break
        else:
            print("Enter a valid selection.")


    while gender == 'female':
        if job_type == 'sedentary':
            female_bmr += 300
            print("...calculating your new bmr")
            time.sleep(2)
            print("Your new bmr is", round(female_bmr,2), "kcal.")
            break
        elif job_type == 'sedentary-active':
            female_bmr += 500
            print("...calculating your new bmr")
            time.sleep(2)
            print("Your new bmr is", round(female_bmr,2), "kcal.")
            break
        elif job_type == 'active-sedentary':
            female_bmr += 700
            print("...calculating your new bmr")
            time.sleep(2)
            print("Your new bmr is", round(female_bmr,2), "kcal.")
            break
        elif job_type == 'active':
            female_bmr += 900
            print("...calculating your new bmr")
            time.sleep(2)
            print("Your new bmr is", round(female_bmr,2), "kcal.")
            break
        else:
            print("Enter a valid selection.")


    # adding more calories or keeping the same based on minutes of cardio per week 
    # and how many weight training session per week
    
if __name__ == "__main__":
    main()
